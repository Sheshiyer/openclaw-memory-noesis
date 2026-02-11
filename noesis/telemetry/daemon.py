"""
Prana Stream - Background Daemon
प्राण दैत्य — The vital spirit that watches in the background

Background process that:
1. Creates and monitors the named pipe (FIFO)
2. Reads events from FIFO
3. Broadcasts to connected clients (future: websocket)
4. Manages its own lifecycle via PID file
"""

import os
import sys
import stat
import signal
import time
import json
import select
from pathlib import Path
from typing import Optional, Callable
from datetime import datetime

from .schema import get_fifo_path, get_pid_path, PranaEvent


class PranaDaemon:
    """Background daemon for real-time event streaming."""
    
    def __init__(
        self,
        fifo_path: Optional[Path] = None,
        pid_path: Optional[Path] = None,
        on_event: Optional[Callable[[PranaEvent], None]] = None
    ):
        self.fifo_path = fifo_path or get_fifo_path()
        self.pid_path = pid_path or get_pid_path()
        self.on_event = on_event or self._default_handler
        self.running = False
        self._fifo_fd = None
    
    def _default_handler(self, event: PranaEvent) -> None:
        """Default event handler - print to stdout."""
        guna_colors = {"sattvic": "🟢", "rajasic": "🟠", "tamasic": "🔴"}
        guna_icon = guna_colors.get(event.guna_state, "⚪")
        
        ts = event.timestamp[11:19] if len(event.timestamp) > 19 else event.timestamp
        agent = event.agent_id or "system"
        
        print(f"[{ts}] {guna_icon} {event.event_type:12} │ {event.kosha_layer:12} │ {agent}")
    
    def _create_fifo(self) -> None:
        """Create the named pipe if it doesn't exist."""
        self.fifo_path.parent.mkdir(parents=True, exist_ok=True)
        
        if self.fifo_path.exists():
            # Remove if it's not a FIFO
            if not stat.S_ISFIFO(self.fifo_path.stat().st_mode):
                self.fifo_path.unlink()
                os.mkfifo(str(self.fifo_path))
        else:
            os.mkfifo(str(self.fifo_path))
    
    def _write_pid(self) -> None:
        """Write PID file."""
        self.pid_path.parent.mkdir(parents=True, exist_ok=True)
        self.pid_path.write_text(str(os.getpid()))
    
    def _remove_pid(self) -> None:
        """Remove PID file."""
        if self.pid_path.exists():
            self.pid_path.unlink()
    
    def _cleanup(self) -> None:
        """Clean up resources."""
        self._remove_pid()
        if self._fifo_fd is not None:
            try:
                os.close(self._fifo_fd)
            except Exception:
                pass
        # Don't remove FIFO - other processes may be writing
    
    def _signal_handler(self, signum, frame):
        """Handle termination signals."""
        self.running = False
    
    def start(self, foreground: bool = False) -> int:
        """
        Start the daemon.
        
        Args:
            foreground: If True, run in foreground (for debugging)
        
        Returns:
            PID of the daemon process
        """
        # Check if already running
        if self.pid_path.exists():
            try:
                pid = int(self.pid_path.read_text().strip())
                # Check if process exists
                os.kill(pid, 0)
                print(f"Prana daemon already running (PID: {pid})")
                return pid
            except (ProcessLookupError, ValueError):
                # Stale PID file
                self._remove_pid()
        
        if not foreground:
            # Fork to background
            pid = os.fork()
            if pid > 0:
                # Parent process
                print(f"Prana daemon started (PID: {pid})")
                return pid
            
            # Child process - detach
            os.setsid()
            
            # Fork again to prevent zombie
            pid = os.fork()
            if pid > 0:
                os._exit(0)
            
            # Redirect stdio
            sys.stdin.close()
            sys.stdout = open('/dev/null', 'w')
            sys.stderr = open('/dev/null', 'w')
        
        # Setup
        self._create_fifo()
        self._write_pid()
        
        # Signal handlers
        signal.signal(signal.SIGTERM, self._signal_handler)
        signal.signal(signal.SIGINT, self._signal_handler)
        
        self.running = True
        self._run_loop()
        
        self._cleanup()
        return os.getpid()
    
    def _run_loop(self) -> None:
        """Main event loop - read from FIFO and dispatch events."""
        buffer = ""
        
        while self.running:
            try:
                # Open FIFO for reading (blocks until writer connects)
                # Use O_RDONLY | O_NONBLOCK to prevent blocking forever
                self._fifo_fd = os.open(str(self.fifo_path), os.O_RDONLY | os.O_NONBLOCK)
                
                while self.running:
                    # Use select with timeout to allow checking self.running
                    readable, _, _ = select.select([self._fifo_fd], [], [], 1.0)
                    
                    if not readable:
                        continue
                    
                    try:
                        data = os.read(self._fifo_fd, 4096)
                        if not data:
                            # Writer closed - reopen FIFO
                            break
                        
                        buffer += data.decode('utf-8')
                        
                        # Process complete lines
                        while '\n' in buffer:
                            line, buffer = buffer.split('\n', 1)
                            if line.strip():
                                self._process_line(line)
                    
                    except (OSError, BlockingIOError):
                        continue
                
                os.close(self._fifo_fd)
                self._fifo_fd = None
            
            except Exception as e:
                if self.running:
                    # Brief sleep before retry
                    time.sleep(0.5)
    
    def _process_line(self, line: str) -> None:
        """Process a single line from FIFO."""
        try:
            event = PranaEvent.from_json(line)
            self.on_event(event)
        except json.JSONDecodeError:
            pass  # Ignore malformed data
        except Exception as e:
            pass  # Don't crash on handler errors
    
    @staticmethod
    def stop(pid_path: Optional[Path] = None) -> bool:
        """
        Stop the daemon.
        
        Returns:
            True if daemon was stopped, False if not running
        """
        pid_path = pid_path or get_pid_path()
        
        if not pid_path.exists():
            print("Prana daemon not running")
            return False
        
        try:
            pid = int(pid_path.read_text().strip())
            os.kill(pid, signal.SIGTERM)
            
            # Wait for process to exit
            for _ in range(10):
                try:
                    os.kill(pid, 0)
                    time.sleep(0.1)
                except ProcessLookupError:
                    break
            
            # Clean up PID file
            if pid_path.exists():
                pid_path.unlink()
            
            print(f"Prana daemon stopped (PID: {pid})")
            return True
        
        except ProcessLookupError:
            # Process doesn't exist - clean up stale PID
            pid_path.unlink()
            print("Prana daemon was not running (cleaned up stale PID)")
            return False
        
        except ValueError:
            print("Invalid PID file")
            return False
    
    @staticmethod
    def status(pid_path: Optional[Path] = None) -> dict:
        """Get daemon status."""
        pid_path = pid_path or get_pid_path()
        fifo_path = get_fifo_path()
        
        result = {
            "running": False,
            "pid": None,
            "fifo_exists": fifo_path.exists(),
            "pid_file": str(pid_path),
            "fifo_path": str(fifo_path)
        }
        
        if pid_path.exists():
            try:
                pid = int(pid_path.read_text().strip())
                os.kill(pid, 0)  # Check if process exists
                result["running"] = True
                result["pid"] = pid
            except (ProcessLookupError, ValueError):
                pass
        
        return result


def start_daemon(foreground: bool = False) -> int:
    """Start the Prana daemon."""
    daemon = PranaDaemon()
    return daemon.start(foreground=foreground)


def stop_daemon() -> bool:
    """Stop the Prana daemon."""
    return PranaDaemon.stop()


def daemon_status() -> dict:
    """Get daemon status."""
    return PranaDaemon.status()


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Prana Stream Daemon")
    parser.add_argument("action", choices=["start", "stop", "status", "foreground"],
                       help="Action to perform")
    args = parser.parse_args()
    
    if args.action == "start":
        start_daemon()
    elif args.action == "stop":
        stop_daemon()
    elif args.action == "status":
        status = daemon_status()
        print(json.dumps(status, indent=2))
    elif args.action == "foreground":
        print("Starting Prana daemon in foreground (Ctrl+C to stop)...")
        start_daemon(foreground=True)
