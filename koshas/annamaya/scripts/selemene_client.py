#!/usr/bin/env python3
"""
selemene_client.py — Python client for Selemene Noesis API

High-precision consciousness calculation engine.
Base URL: https://selemene.tryambakam.space

Usage:
    from selemene_client import SelemeneClient
    
    client = SelemeneClient(api_key=os.getenv("NOESIS_API_KEY"))
    result = client.numerology({"date": "1991-08-13", "name": "Test"})
"""

import os
import json
from datetime import datetime
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

# ═══════════════════════════════════════════════════════════════════════════════
# Configuration
# ═══════════════════════════════════════════════════════════════════════════════

DEFAULT_BASE_URL = "https://selemene.tryambakam.space"
DEFAULT_TIMEOUT = 30

# ═══════════════════════════════════════════════════════════════════════════════
# Data Classes
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class BirthData:
    """Birth data for engine calculations."""
    date: str  # YYYY-MM-DD
    time: Optional[str] = None  # HH:MM
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    timezone: Optional[str] = None
    name: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        result = {"date": self.date}
        if self.time:
            result["time"] = self.time
        if self.latitude is not None:
            result["latitude"] = self.latitude
        if self.longitude is not None:
            result["longitude"] = self.longitude
        if self.timezone:
            result["timezone"] = self.timezone
        if self.name:
            result["name"] = self.name
        return result


@dataclass
class EngineResult:
    """Result from an engine calculation."""
    engine_id: str
    result: Dict[str, Any]
    witness_prompt: Optional[str] = None
    consciousness_level: int = 0
    metadata: Optional[Dict[str, Any]] = None
    
    @classmethod
    def from_response(cls, data: Dict[str, Any]) -> "EngineResult":
        return cls(
            engine_id=data.get("engine_id", "unknown"),
            result=data.get("result", {}),
            witness_prompt=data.get("witness_prompt"),
            consciousness_level=data.get("consciousness_level", 0),
            metadata=data.get("metadata")
        )


@dataclass
class WorkflowResult:
    """Result from a workflow execution."""
    workflow_id: str
    results: Dict[str, EngineResult]
    synthesis: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


# ═══════════════════════════════════════════════════════════════════════════════
# Exceptions
# ═══════════════════════════════════════════════════════════════════════════════

class SelemeneError(Exception):
    """Base exception for Selemene client errors."""
    pass


class AuthenticationError(SelemeneError):
    """API key invalid or missing."""
    pass


class RateLimitError(SelemeneError):
    """Rate limit exceeded."""
    pass


class CalculationError(SelemeneError):
    """Engine calculation failed."""
    pass


# ═══════════════════════════════════════════════════════════════════════════════
# Client
# ═══════════════════════════════════════════════════════════════════════════════

class SelemeneClient:
    """
    Client for Selemene Noesis API.
    
    Example:
        client = SelemeneClient(api_key="nk_your_key")
        
        # Individual engine
        numerology = client.numerology({"date": "1991-08-13", "name": "Shesh"})
        
        # Workflow
        daily = client.workflow("daily-practice", birth_data)
    """
    
    # Available engines
    ENGINES = [
        "biofield", "biorhythm", "gene-keys", "human-design",
        "numerology", "panchanga", "vedic-clock", "vimshottari"
    ]
    
    # Available workflows
    WORKFLOWS = [
        "birth-blueprint", "daily-practice", "decision-support",
        "self-inquiry", "creative-expression", "full-spectrum"
    ]
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: str = DEFAULT_BASE_URL,
        timeout: int = DEFAULT_TIMEOUT
    ):
        self.api_key = api_key or os.getenv("NOESIS_API_KEY")
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        
        if not self.api_key:
            raise SelemeneError(
                "API key required. Set NOESIS_API_KEY env var or pass api_key parameter."
            )
    
    # ═══════════════════════════════════════════════════════════════════════════
    # Core HTTP
    # ═══════════════════════════════════════════════════════════════════════════
    
    def _request(
        self,
        method: str,
        path: str,
        data: Optional[Dict[str, Any]] = None,
        auth: bool = True
    ) -> Dict[str, Any]:
        """Make HTTP request to API."""
        url = f"{self.base_url}{path}"
        
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "SelemeneClient/1.0 (Tryambakam Noesis)",
            "Accept": "application/json"
        }
        if auth:
            headers["X-API-Key"] = self.api_key
        
        body = json.dumps(data).encode("utf-8") if data else None
        
        req = Request(url, data=body, headers=headers, method=method)
        
        try:
            with urlopen(req, timeout=self.timeout) as response:
                return json.loads(response.read().decode("utf-8"))
        except HTTPError as e:
            error_body = e.read().decode("utf-8")
            try:
                error_data = json.loads(error_body)
                error_msg = error_data.get("error", str(e))
            except json.JSONDecodeError:
                error_msg = error_body or str(e)
            
            if e.code == 401:
                raise AuthenticationError(error_msg)
            elif e.code == 429:
                raise RateLimitError(error_msg)
            elif e.code == 500:
                raise CalculationError(error_msg)
            else:
                raise SelemeneError(f"HTTP {e.code}: {error_msg}")
        except URLError as e:
            raise SelemeneError(f"Connection error: {e.reason}")
    
    def _get(self, path: str, auth: bool = True) -> Dict[str, Any]:
        return self._request("GET", path, auth=auth)
    
    def _post(self, path: str, data: Dict[str, Any], auth: bool = True) -> Dict[str, Any]:
        return self._request("POST", path, data=data, auth=auth)
    
    # ═══════════════════════════════════════════════════════════════════════════
    # Health & Discovery
    # ═══════════════════════════════════════════════════════════════════════════
    
    def health(self) -> Dict[str, Any]:
        """Check API health (no auth required)."""
        return self._get("/health/live", auth=False)
    
    def list_engines(self) -> List[str]:
        """List available engines."""
        response = self._get("/api/v1/engines")
        return response.get("engines", [])
    
    def list_workflows(self) -> List[str]:
        """List available workflows."""
        response = self._get("/api/v1/workflows")
        return [w.get("id") for w in response.get("workflows", [])]
    
    def engine_info(self, engine_id: str) -> Dict[str, Any]:
        """Get detailed info about an engine."""
        return self._get(f"/api/v1/engines/{engine_id}/info")
    
    # ═══════════════════════════════════════════════════════════════════════════
    # Engine Calculations
    # ═══════════════════════════════════════════════════════════════════════════
    
    def _normalize_birth_data(self, birth_data: Any) -> Dict[str, Any]:
        """Convert birth_data to dict format."""
        if isinstance(birth_data, BirthData):
            return birth_data.to_dict()
        elif isinstance(birth_data, dict):
            return birth_data
        else:
            raise SelemeneError(f"Invalid birth_data type: {type(birth_data)}")
    
    def calculate(
        self,
        engine_id: str,
        birth_data: Optional[Any] = None,
        current_time: Optional[str] = None,
        precision: str = "Standard",
        options: Optional[Dict[str, Any]] = None
    ) -> EngineResult:
        """
        Generic engine calculation.
        
        Args:
            engine_id: Engine to use (e.g., "numerology", "biorhythm")
            birth_data: Birth data dict or BirthData object
            current_time: ISO timestamp (defaults to now)
            precision: "standard", "high", or "extreme"
            options: Engine-specific options
        
        Returns:
            EngineResult with calculation output
        """
        payload: Dict[str, Any] = {"precision": precision}
        
        if birth_data:
            payload["birth_data"] = self._normalize_birth_data(birth_data)
        
        if current_time:
            payload["current_time"] = current_time
        
        if options:
            payload["options"] = options
        
        response = self._post(f"/api/v1/engines/{engine_id}/calculate", payload)
        return EngineResult.from_response(response)
    
    # ═══════════════════════════════════════════════════════════════════════════
    # Convenience Methods (One per Engine)
    # ═══════════════════════════════════════════════════════════════════════════
    
    def numerology(self, birth_data: Any) -> EngineResult:
        """
        Numerology calculation.
        Required: date, name
        Returns: life_path, expression, soul_urge, personality, birthday
        """
        return self.calculate("numerology", birth_data)
    
    def biorhythm(self, birth_data: Any) -> EngineResult:
        """
        Biorhythm calculation.
        Required: date
        Returns: physical, emotional, intellectual cycles + forecast
        """
        return self.calculate("biorhythm", birth_data)
    
    def human_design(self, birth_data: Any) -> EngineResult:
        """
        Human Design calculation.
        Required: date, time, latitude, longitude, timezone
        Returns: type, strategy, authority, profile, centers, gates
        """
        return self.calculate("human-design", birth_data)
    
    def gene_keys(self, birth_data: Any) -> EngineResult:
        """
        Gene Keys calculation.
        Required: date, time, latitude, longitude, timezone
        Returns: 4 activation sequences with Shadow/Gift/Siddhi
        """
        return self.calculate("gene-keys", birth_data)
    
    def vimshottari(self, birth_data: Any) -> EngineResult:
        """
        Vimshottari Dasha calculation.
        Required: date, time, latitude, longitude, timezone
        Returns: Mahadasha, Antardasha, Pratyantardasha periods
        """
        return self.calculate("vimshottari", birth_data)
    
    def panchanga(self, birth_data: Any) -> EngineResult:
        """
        Panchanga calculation.
        Required: date, latitude, longitude, timezone
        Returns: tithi, nakshatra, yoga, karana, vara
        """
        return self.calculate("panchanga", birth_data)
    
    def vedic_clock(self, current_time: Optional[str] = None) -> EngineResult:
        """
        Vedic Clock calculation.
        No birth data needed — uses current time.
        Returns: TCM organ clock, Ayurvedic dosha timing
        """
        return self.calculate("vedic-clock", current_time=current_time)
    
    def biofield(self, birth_data: Any) -> EngineResult:
        """
        Biofield calculation (stub).
        Required: date
        Returns: Chakra readings
        """
        return self.calculate("biofield", birth_data)
    
    # ═══════════════════════════════════════════════════════════════════════════
    # Workflows
    # ═══════════════════════════════════════════════════════════════════════════
    
    def workflow(
        self,
        workflow_id: str,
        birth_data: Optional[Any] = None,
        current_time: Optional[str] = None,
        options: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Execute a workflow (multi-engine synthesis).
        
        Available workflows:
            - birth-blueprint: numerology + HD + vimshottari
            - daily-practice: panchanga + vedic-clock + biorhythm
            - decision-support: tarot + i-ching + HD authority
            - self-inquiry: gene-keys + enneagram
            - creative-expression: sigil-forge + sacred-geometry
            - full-spectrum: all engines
        """
        payload: Dict[str, Any] = {}
        
        if birth_data:
            payload["birth_data"] = self._normalize_birth_data(birth_data)
        
        if current_time:
            payload["current_time"] = current_time
        
        if options:
            payload["options"] = options
        
        return self._post(f"/api/v1/workflows/{workflow_id}/execute", payload)
    
    def birth_blueprint(self, birth_data: Any) -> Dict[str, Any]:
        """Core identity mapping: numerology + HD + vimshottari."""
        return self.workflow("birth-blueprint", birth_data)
    
    def daily_practice(self, birth_data: Any) -> Dict[str, Any]:
        """Daily rhythm: panchanga + vedic-clock + biorhythm."""
        return self.workflow("daily-practice", birth_data)
    
    def full_spectrum(self, birth_data: Any) -> Dict[str, Any]:
        """Complete consciousness portrait: all engines."""
        return self.workflow("full-spectrum", birth_data)


# ═══════════════════════════════════════════════════════════════════════════════
# Shesh's Birth Data (Convenience)
# ═══════════════════════════════════════════════════════════════════════════════

SHESH_BIRTH_DATA = BirthData(
    date="1991-08-13",
    time="13:31",
    latitude=12.9716,
    longitude=77.5946,
    timezone="Asia/Kolkata",
    name="Shesh Iyer"
)


# ═══════════════════════════════════════════════════════════════════════════════
# CLI Interface
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    """CLI interface for testing."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Selemene API Client")
    parser.add_argument("--health", action="store_true", help="Check API health")
    parser.add_argument("--engines", action="store_true", help="List engines")
    parser.add_argument("--workflows", action="store_true", help="List workflows")
    parser.add_argument("--engine", type=str, help="Calculate with specific engine")
    parser.add_argument("--workflow", type=str, help="Execute specific workflow")
    parser.add_argument("--date", type=str, default="1991-08-13", help="Birth date (YYYY-MM-DD)")
    parser.add_argument("--time", type=str, default="13:31", help="Birth time (HH:MM)")
    parser.add_argument("--name", type=str, default="Shesh Iyer", help="Name for numerology")
    
    args = parser.parse_args()
    
    try:
        client = SelemeneClient()
        
        if args.health:
            result = client.health()
            print(json.dumps(result, indent=2))
        
        elif args.engines:
            engines = client.list_engines()
            print("Available engines:")
            for e in engines:
                print(f"  - {e}")
        
        elif args.workflows:
            workflows = client.list_workflows()
            print("Available workflows:")
            for w in workflows:
                print(f"  - {w}")
        
        elif args.engine:
            birth_data = BirthData(
                date=args.date,
                time=args.time,
                latitude=12.9716,
                longitude=77.5946,
                timezone="Asia/Kolkata",
                name=args.name
            )
            result = client.calculate(args.engine, birth_data)
            print(f"Engine: {result.engine_id}")
            print(f"Result: {json.dumps(result.result, indent=2)}")
            if result.witness_prompt:
                print(f"\nWitness Prompt: {result.witness_prompt}")
        
        elif args.workflow:
            birth_data = BirthData(
                date=args.date,
                time=args.time,
                latitude=12.9716,
                longitude=77.5946,
                timezone="Asia/Kolkata",
                name=args.name
            )
            result = client.workflow(args.workflow, birth_data)
            print(json.dumps(result, indent=2))
        
        else:
            parser.print_help()
    
    except SelemeneError as e:
        print(f"Error: {e}")
        exit(1)


if __name__ == "__main__":
    main()
