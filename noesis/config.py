"""
Noesis Configuration Management
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Loads configuration from:
1. noesis.toml (project root)
2. Environment variables (NOESIS_*)
3. CLI arguments (highest priority)
"""

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

# Try tomllib (Python 3.11+) or fall back to manual parsing
try:
    import tomllib
except ImportError:
    tomllib = None  # type: ignore


@dataclass
class SelemeneConfig:
    """Selemene Engine API configuration."""
    base_url: str = "https://selemene.tryambakam.space"
    api_key: Optional[str] = None
    timeout: int = 30
    user_agent: str = "Noesis/0.1.0"


@dataclass
class AgentConfig:
    """Agent installation configuration."""
    default_tier: str = "core"
    auto_fetch_selemene: bool = True


@dataclass
class Config:
    """Main Noesis configuration."""
    version: str = "0.1.0"
    koshas_root: Path = field(default_factory=lambda: Path("./koshas"))
    brahmasthana: Path = field(default_factory=lambda: Path("./koshas/brahmasthana"))
    selemene: SelemeneConfig = field(default_factory=SelemeneConfig)
    agents: AgentConfig = field(default_factory=AgentConfig)
    
    def __post_init__(self):
        # Convert strings to Path if needed
        if isinstance(self.koshas_root, str):
            self.koshas_root = Path(self.koshas_root)
        if isinstance(self.brahmasthana, str):
            self.brahmasthana = Path(self.brahmasthana)


def find_config_file(start_path: Optional[Path] = None) -> Optional[Path]:
    """Find noesis.toml by walking up from start_path."""
    if start_path is None:
        start_path = Path.cwd()
    
    current = start_path.resolve()
    
    for _ in range(10):  # Max 10 levels up
        config_path = current / "noesis.toml"
        if config_path.exists():
            return config_path
        
        parent = current.parent
        if parent == current:  # Reached root
            break
        current = parent
    
    return None


def parse_toml_simple(content: str) -> dict:
    """Simple TOML parser for basic key=value and [sections]."""
    result: dict = {}
    current_section: Optional[str] = None
    
    for line in content.splitlines():
        line = line.strip()
        
        # Skip empty lines and comments
        if not line or line.startswith("#"):
            continue
        
        # Section header
        if line.startswith("[") and line.endswith("]"):
            current_section = line[1:-1]
            if current_section not in result:
                result[current_section] = {}
            continue
        
        # Key = value
        if "=" in line:
            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip()
            
            # Remove quotes from strings
            if (value.startswith('"') and value.endswith('"')) or \
               (value.startswith("'") and value.endswith("'")):
                value = value[1:-1]
            # Parse booleans
            elif value.lower() == "true":
                value = True
            elif value.lower() == "false":
                value = False
            # Parse integers
            elif value.isdigit():
                value = int(value)
            
            if current_section:
                result[current_section][key] = value
            else:
                result[key] = value
    
    return result


def load_config(config_path: Optional[Path] = None) -> Config:
    """
    Load configuration from noesis.toml and environment variables.
    
    Priority (highest wins):
    1. Environment variables (NOESIS_*)
    2. noesis.toml file
    3. Defaults
    """
    config = Config()
    
    # Find and load config file
    if config_path is None:
        config_path = find_config_file()
    
    if config_path and config_path.exists():
        content = config_path.read_text()
        
        if tomllib:
            data = tomllib.loads(content)
        else:
            data = parse_toml_simple(content)
        
        # Apply noesis section
        if "noesis" in data:
            noesis_data = data["noesis"]
            if "koshas_root" in noesis_data:
                config.koshas_root = Path(noesis_data["koshas_root"])
            if "brahmasthana" in noesis_data:
                config.brahmasthana = Path(noesis_data["brahmasthana"])
        
        # Apply selemene section
        if "selemene" in data:
            sel_data = data["selemene"]
            if "base_url" in sel_data:
                config.selemene.base_url = sel_data["base_url"]
            if "timeout" in sel_data:
                config.selemene.timeout = int(sel_data["timeout"])
            if "user_agent" in sel_data:
                config.selemene.user_agent = sel_data["user_agent"]
        
        # Apply agents section
        if "agents" in data:
            agent_data = data["agents"]
            if "default_tier" in agent_data:
                config.agents.default_tier = agent_data["default_tier"]
            if "auto_fetch_selemene" in agent_data:
                config.agents.auto_fetch_selemene = bool(agent_data["auto_fetch_selemene"])
    
    # Override with environment variables
    if os.environ.get("NOESIS_API_KEY"):
        config.selemene.api_key = os.environ["NOESIS_API_KEY"]
    
    if os.environ.get("NOESIS_KOSHAS_ROOT"):
        config.koshas_root = Path(os.environ["NOESIS_KOSHAS_ROOT"])
    
    if os.environ.get("NOESIS_BRAHMASTHANA"):
        config.brahmasthana = Path(os.environ["NOESIS_BRAHMASTHANA"])
    
    if os.environ.get("NOESIS_DEFAULT_TIER"):
        config.agents.default_tier = os.environ["NOESIS_DEFAULT_TIER"]
    
    return config


def resolve_paths(config: Config, base_path: Optional[Path] = None) -> Config:
    """Resolve relative paths in config to absolute paths."""
    if base_path is None:
        base_path = Path.cwd()
    
    if not config.koshas_root.is_absolute():
        config.koshas_root = (base_path / config.koshas_root).resolve()
    
    if not config.brahmasthana.is_absolute():
        config.brahmasthana = (base_path / config.brahmasthana).resolve()
    
    return config
