"""
Pytest configuration and fixtures
"""

import pytest
from pathlib import Path


@pytest.fixture
def koshas_root():
    """Return the koshas root directory."""
    return Path(__file__).parent.parent / "koshas"


@pytest.fixture
def brahmasthana(koshas_root):
    """Return the brahmasthana directory."""
    return koshas_root / "brahmasthana"
