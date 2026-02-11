"""
Tryambakam Noesis Multi-Framework Adapters

This package allows any AI framework (LangChain, CrewAI, OpenAI, Anthropic, etc.)
to "wear" the Tryambakam Noesis architecture by reading agent manifests and 
generating framework-specific configurations.

Architecture:
- Each adapter reads MANIFEST.yaml (or falls back to SOUL.md/IDENTITY.md/TOOLS.md)
- Adapters generate framework-specific tool definitions and system prompts
- Context assembly uses the Prana system for unified consciousness streams

Usage:
    from adapters import langchain_adapter, crewai_adapter, openai_adapter, anthropic_adapter
    
    # Load an agent
    agent_path = Path("koshas/annamaya/agents/noesis-vishwakarma")
    
    # Generate for different frameworks
    langchain_tools = langchain_adapter.generate_langchain_tools(agent_path)
    crewai_agent = crewai_adapter.generate_crewai_agent(agent_path)
    openai_functions = openai_adapter.generate_openai_functions(agent_path)
    anthropic_tools = anthropic_adapter.generate_anthropic_tools(agent_path)
"""

from . import langchain_adapter
from . import crewai_adapter
from . import openai_adapter
from . import anthropic_adapter

__all__ = [
    'langchain_adapter',
    'crewai_adapter', 
    'openai_adapter',
    'anthropic_adapter',
]

__version__ = "1.0.0"
