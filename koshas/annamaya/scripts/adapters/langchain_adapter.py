"""
LangChain Adapter for Tryambakam Noesis Architecture

Converts Noesis agent definitions into LangChain-compatible tools and agents.
Reads MANIFEST.yaml or falls back to SOUL.md/IDENTITY.md structure.
"""

import yaml
from pathlib import Path
from typing import Dict, List, Optional, Any
import json


def load_manifest(agent_path: Path) -> dict:
    """
    Load agent manifest from MANIFEST.yaml or construct from agent files.
    
    Args:
        agent_path: Path to agent directory (e.g., koshas/annamaya/agents/noesis-vishwakarma)
    
    Returns:
        Dictionary containing agent configuration (normalized structure)
    """
    agent_path = Path(agent_path)
    
    # Try to load MANIFEST.yaml first
    manifest_file = agent_path / "MANIFEST.yaml"
    if manifest_file.exists():
        with open(manifest_file, 'r') as f:
            raw_manifest = yaml.safe_load(f)
        
        # Normalize to expected structure
        manifest = {
            "name": raw_manifest.get("display_name", raw_manifest.get("agent_id", agent_path.name)),
            "agent_id": raw_manifest.get("agent_id", agent_path.name),
            "agent_path": str(agent_path),
            "required_context": [str(agent_path / f) for f in raw_manifest.get("required_context", [])],
            "optional_context": [str(agent_path / f) for f in raw_manifest.get("optional_context", [])],
            "capabilities": raw_manifest.get("capabilities", []),
            "tools": raw_manifest.get("tools", []),
            "metadata": {
                "emoji": raw_manifest.get("emoji", "🤖"),
                "description": raw_manifest.get("description", ""),
                "kosha_alignment": raw_manifest.get("kosha_alignment", ""),
                "version": raw_manifest.get("version", "1.0.0")
            }
        }
        return manifest
    
    # Fall back to constructing from individual files
    manifest = {
        "name": agent_path.name,
        "agent_id": agent_path.name,
        "agent_path": str(agent_path),
        "required_context": [],
        "capabilities": [],
        "metadata": {}
    }
    
    # Read IDENTITY.md for metadata
    identity_file = agent_path / "IDENTITY.md"
    if identity_file.exists():
        identity_content = identity_file.read_text()
        manifest["metadata"]["identity"] = identity_content
        
        # Parse basic metadata from IDENTITY.md
        for line in identity_content.split('\n'):
            if line.startswith('- **Name:**'):
                manifest["name"] = line.split('**Name:**')[1].strip()
            elif line.startswith('- **Mission:**'):
                manifest["metadata"]["mission"] = line.split('**Mission:**')[1].strip()
    
    # Track available context files
    for context_file in ["SOUL.md", "IDENTITY.md", "TOOLS.md", "MEMORY.md", "USER.md"]:
        if (agent_path / context_file).exists():
            manifest["required_context"].append(str(agent_path / context_file))
    
    return manifest


def generate_context(manifest: dict) -> str:
    """
    Generate unified context string from required context files.
    
    Args:
        manifest: Agent manifest dictionary
    
    Returns:
        Concatenated context string suitable for system prompts
    """
    context_parts = []
    
    for context_file in manifest.get("required_context", []):
        context_path = Path(context_file)
        if context_path.exists():
            content = context_path.read_text()
            context_parts.append(f"# {context_path.name}\n\n{content}\n")
    
    return "\n---\n\n".join(context_parts)


def generate_langchain_tools(agent_path: Path) -> List[Dict[str, Any]]:
    """
    Generate LangChain Tool definitions from agent manifest.
    
    Args:
        agent_path: Path to agent directory
    
    Returns:
        List of LangChain tool definitions (dicts with name, description, func, args_schema)
    """
    manifest = load_manifest(agent_path)
    tools = []
    
    # Read TOOLS.md if available
    tools_file = Path(agent_path) / "TOOLS.md"
    if tools_file.exists():
        tools_content = tools_file.read_text()
        
        # Parse tools from markdown (simple heuristic)
        # Look for sections like "## Tool Name" or "### Tool Name"
        current_tool = None
        for line in tools_content.split('\n'):
            if line.startswith('##') or line.startswith('###'):
                # Save previous tool if exists
                if current_tool:
                    tools.append(current_tool)
                
                # Start new tool
                tool_name = line.lstrip('#').strip()
                current_tool = {
                    "name": tool_name.lower().replace(' ', '_'),
                    "description": tool_name,
                    "parameters": {
                        "type": "object",
                        "properties": {},
                        "required": []
                    }
                }
            elif current_tool and line.strip() and not line.startswith('#'):
                # Add to description
                current_tool["description"] += f" {line.strip()}"
        
        # Add last tool
        if current_tool:
            tools.append(current_tool)
    
    # If no tools found, create a default agent interaction tool
    if not tools:
        tools.append({
            "name": f"{manifest['name'].lower().replace(' ', '_')}_agent",
            "description": f"Interact with {manifest['name']} agent. {manifest.get('metadata', {}).get('mission', '')}",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The query or task for the agent"
                    }
                },
                "required": ["query"]
            }
        })
    
    return tools


class NoesisAgent:
    """
    LangChain-compatible Noesis Agent wrapper.
    
    Usage:
        agent = NoesisAgent(agent_path)
        result = agent.run("Build a new feature")
    """
    
    def __init__(self, agent_path: Path):
        """
        Initialize Noesis Agent with context from manifest.
        
        Args:
            agent_path: Path to agent directory
        """
        self.agent_path = Path(agent_path)
        self.manifest = load_manifest(agent_path)
        self.context = generate_context(self.manifest)
        self.tools = generate_langchain_tools(agent_path)
        self.name = self.manifest.get("name", agent_path.name)
    
    def get_system_prompt(self) -> str:
        """Get the complete system prompt including all context."""
        return f"""You are {self.name}, a Noesis agent.

{self.context}

Use your capabilities and context to assist with tasks aligned with your mission.
"""
    
    def get_tools(self) -> List[Dict[str, Any]]:
        """Get LangChain tool definitions."""
        return self.tools
    
    def run(self, query: str) -> str:
        """
        Execute a query against this agent.
        
        Args:
            query: The task or question for the agent
        
        Returns:
            Agent response (placeholder - integrate with actual LangChain execution)
        """
        # Placeholder - in real implementation, this would use LangChain's agent execution
        return f"[{self.name}] Processing: {query}\n\nContext loaded from: {len(self.manifest.get('required_context', []))} files"
    
    def to_langchain_config(self) -> dict:
        """
        Export complete configuration for LangChain agent creation.
        
        Returns:
            Dictionary with all necessary LangChain agent parameters
        """
        return {
            "name": self.name,
            "system_prompt": self.get_system_prompt(),
            "tools": self.tools,
            "metadata": self.manifest.get("metadata", {}),
            "agent_type": "openai-functions",  # or "conversational-react-description"
        }


def test_langchain_adapter():
    """Test the LangChain adapter with a real agent."""
    # Find an agent to test with
    test_agent_path = Path(__file__).parent.parent.parent / "agents" / "noesis-vishwakarma"
    
    if not test_agent_path.exists():
        print(f"❌ Test agent not found at: {test_agent_path}")
        return
    
    print(f"🔧 Testing LangChain Adapter with: {test_agent_path.name}\n")
    
    # Load manifest
    manifest = load_manifest(test_agent_path)
    print(f"✅ Loaded manifest: {manifest['name']}")
    print(f"   Context files: {len(manifest.get('required_context', []))}")
    
    # Generate context
    context = generate_context(manifest)
    print(f"   Context length: {len(context)} characters")
    
    # Generate tools
    tools = generate_langchain_tools(test_agent_path)
    print(f"   Tools generated: {len(tools)}")
    for tool in tools:
        print(f"      - {tool['name']}: {tool['description'][:60]}...")
    
    # Create agent instance
    print("\n🤖 Creating NoesisAgent instance...")
    agent = NoesisAgent(test_agent_path)
    print(f"   Agent name: {agent.name}")
    print(f"   System prompt length: {len(agent.get_system_prompt())} characters")
    
    # Test run
    print("\n🎯 Testing agent.run()...")
    result = agent.run("Build a test feature")
    print(f"   Result: {result}")
    
    # Export config
    print("\n📦 Exporting LangChain configuration...")
    config = agent.to_langchain_config()
    print(f"   Config keys: {list(config.keys())}")
    print(f"   Agent type: {config['agent_type']}")
    
    print("\n✨ LangChain adapter test complete!")


if __name__ == "__main__":
    test_langchain_adapter()
