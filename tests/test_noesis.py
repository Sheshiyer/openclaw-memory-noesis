"""
Basic tests for Noesis CLI
"""

import pytest
from pathlib import Path


def test_import():
    """Test that noesis can be imported."""
    import noesis
    assert noesis.__version__ == "0.2.0"


def test_config_loading():
    """Test configuration loading."""
    from noesis.config import Config, load_config
    
    config = load_config()
    assert isinstance(config, Config)
    assert config.selemene.base_url == "https://selemene.tryambakam.space"


def test_tiers_defined():
    """Test that all context tiers are defined."""
    from noesis.core.samskara import TIERS
    
    assert "lite" in TIERS
    assert "core" in TIERS
    assert "standard" in TIERS
    assert "full" in TIERS


def test_vikara_types_defined():
    """Test that vikara types are defined."""
    from noesis.core.vikara import VIKARA_TYPES
    
    assert "STALE_SOUL" in VIKARA_TYPES
    assert "MEMORY_OVERFLOW" in VIKARA_TYPES
    assert "CHECKSUM_MISMATCH" in VIKARA_TYPES


def test_teachings_defined():
    """Test that teaching content is defined."""
    from noesis.core.guru import TEACHINGS
    
    assert "SOUL.md" in TEACHINGS
    assert "IDENTITY.md" in TEACHINGS
    assert "PANCHA-KOSHA.md" in TEACHINGS


def test_cli_parser():
    """Test CLI argument parser."""
    from noesis.cli import create_parser
    
    parser = create_parser()
    
    # Test help doesn't raise
    args = parser.parse_args(["--help"])
    
    # Test version
    args = parser.parse_args(["--version"])


def test_cli_subcommands():
    """Test that subcommands are registered."""
    from noesis.cli import create_parser
    
    parser = create_parser()
    
    # These should not raise
    parser.parse_args(["init"])
    parser.parse_args(["install"])
    parser.parse_args(["health"])
    parser.parse_args(["drift"])
    parser.parse_args(["context"])
    parser.parse_args(["teach", "--list"])
    parser.parse_args(["agents"])
