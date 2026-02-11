"""
CrewAI Adapter for Tryambakam Noesis Architecture

Converts Noesis agent definitions into CrewAI-compatible agents and crews.
Reads MANIFEST.yaml or falls back to SOUL.md/IDENTITY.md structure.
"""

import yaml
from pathlib import Path
from typing import Dict, List, Optional, Any


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
            },
            "crewai": {
                "role": raw_manifest.get("display_name", "Specialist Agent"),
                "goal": raw_manifest.get("description", "Execute specialized tasks"),
                "backstory": f"{raw_manifest.get('emoji', '🤖')} {raw_manifest.get('description', 'An agent from the Tryambakam Noesis consciousness field')}"
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
        "metadata": {},
        "crewai": {
            "role": "Specialist Agent",
            "goal": "Execute specialized tasks",
            "backstory": "An agent from the Tryambakam Noesis consciousness field"
        }
    }
    
    # Read IDENTITY.md for metadata
    identity_file = agent_path / "IDENTITY.md"
    if identity_file.exists():
        identity_content = identity_file.read_text()
        manifest["metadata"]["identity"] = identity_content
        
        # Parse CrewAI-relevant metadata
        for line in identity_content.split('\n'):
            if line.startswith('- **Name:**'):
                manifest["name"] = line.split('**Name:**')[1].strip()
            elif line.startswith('- **Creature:**') or line.startswith('- **Vibe:**'):
                # Use as role
                role = line.split('**')[2].strip()
                manifest["crewai"]["role"] = role
            elif line.startswith('- **Mission:**'):
                manifest["crewai"]["goal"] = line.split('**Mission:**')[1].strip()
    
    # Read SOUL.md for backstory
    soul_file = agent_path / "SOUL.md"
    if soul_file.exists():
        soul_content = soul_file.read_text()
        # Extract first meaningful paragraph as backstory
        lines = [l.strip() for l in soul_content.split('\n') if l.strip() and not l.startswith('#')]
        if lines:
            # Find the "I am..." statement if it exists
            for line in lines:
                if line.startswith('I am'):
                    manifest["crewai"]["backstory"] = line
                    break
            else:
                # Use first non-header line
                manifest["crewai"]["backstory"] = lines[0]
    
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


def generate_crewai_tools(agent_path: Path) -> List[Dict[str, Any]]:
    """
    Generate CrewAI tool definitions from agent manifest.
    
    Args:
        agent_path: Path to agent directory
    
    Returns:
        List of CrewAI tool definitions
    """
    manifest = load_manifest(agent_path)
    tools = []
    
    # Read TOOLS.md if available
    tools_file = Path(agent_path) / "TOOLS.md"
    if tools_file.exists():
        tools_content = tools_file.read_text()
        
        # Parse tools from markdown
        current_tool = None
        for line in tools_content.split('\n'):
            if line.startswith('##') or line.startswith('###'):
                # Save previous tool
                if current_tool:
                    tools.append(current_tool)
                
                # Start new tool
                tool_name = line.lstrip('#').strip()
                current_tool = {
                    "name": tool_name.lower().replace(' ', '_').replace('-', '_'),
                    "description": tool_name,
                    "func": f"execute_{tool_name.lower().replace(' ', '_')}",
                }
            elif current_tool and line.strip() and not line.startswith('#'):
                # Add to description
                current_tool["description"] += f" {line.strip()}"
        
        # Add last tool
        if current_tool:
            tools.append(current_tool)
    
    # Default tool if none found
    if not tools:
        tools.append({
            "name": f"{manifest['name'].lower().replace(' ', '_')}_tool",
            "description": f"Execute tasks with {manifest['name']}",
            "func": "execute_agent_task"
        })
    
    return tools


def generate_crewai_agent(agent_path: Path) -> Dict[str, Any]:
    """
    Generate a complete CrewAI Agent definition from Noesis agent.
    
    Args:
        agent_path: Path to agent directory
    
    Returns:
        Dictionary with CrewAI agent configuration (role, goal, backstory, tools, etc.)
    """
    manifest = load_manifest(agent_path)
    crewai_config = manifest.get("crewai", {})
    tools = generate_crewai_tools(agent_path)
    
    agent_config = {
        "role": crewai_config.get("role", manifest["name"]),
        "goal": crewai_config.get("goal", "Complete assigned tasks with expertise"),
        "backstory": crewai_config.get("backstory", f"A specialist from the Tryambakam Noesis field"),
        "tools": [tool["name"] for tool in tools],
        "verbose": True,
        "allow_delegation": False,
        "max_iter": 15,
        "metadata": {
            "agent_path": str(agent_path),
            "context_files": manifest.get("required_context", []),
            "noesis_agent": True
        }
    }
    
    return agent_config


def create_noesis_crew(agent_paths: List[Path], task_descriptions: Optional[List[str]] = None) -> Dict[str, Any]:
    """
    Create a CrewAI Crew from multiple Noesis agents.
    
    Args:
        agent_paths: List of paths to agent directories
        task_descriptions: Optional list of task descriptions (one per agent)
    
    Returns:
        Dictionary with complete Crew configuration
    """
    agents = []
    tasks = []
    
    for i, agent_path in enumerate(agent_paths):
        agent_config = generate_crewai_agent(agent_path)
        agents.append(agent_config)
        
        # Create task for this agent
        task_desc = task_descriptions[i] if task_descriptions and i < len(task_descriptions) else f"Execute {agent_config['role']} tasks"
        
        tasks.append({
            "description": task_desc,
            "agent": agent_config["role"],
            "expected_output": f"Completed task output from {agent_config['role']}"
        })
    
    crew_config = {
        "agents": agents,
        "tasks": tasks,
        "process": "sequential",  # or "hierarchical"
        "verbose": True,
        "metadata": {
            "noesis_crew": True,
            "agent_count": len(agents)
        }
    }
    
    return crew_config


class NoesisCrewAgent:
    """
    Wrapper class to make Noesis agents compatible with CrewAI.
    
    Usage:
        agent = NoesisCrewAgent(agent_path)
        crew = Crew(agents=[agent.to_crewai()], tasks=[...])
    """
    
    def __init__(self, agent_path: Path):
        """
        Initialize Noesis Crew Agent.
        
        Args:
            agent_path: Path to agent directory
        """
        self.agent_path = Path(agent_path)
        self.manifest = load_manifest(agent_path)
        self.context = generate_context(self.manifest)
        self.config = generate_crewai_agent(agent_path)
    
    def to_crewai(self) -> Dict[str, Any]:
        """Export as CrewAI agent configuration."""
        return self.config
    
    def get_role(self) -> str:
        """Get agent role."""
        return self.config["role"]
    
    def get_goal(self) -> str:
        """Get agent goal."""
        return self.config["goal"]
    
    def get_backstory(self) -> str:
        """Get agent backstory."""
        return self.config["backstory"]
    
    def get_context(self) -> str:
        """Get full agent context."""
        return self.context


def test_crewai_adapter():
    """Test the CrewAI adapter with a real agent."""
    # Find an agent to test with
    test_agent_path = Path(__file__).parent.parent.parent / "agents" / "noesis-vishwakarma"
    
    if not test_agent_path.exists():
        print(f"❌ Test agent not found at: {test_agent_path}")
        return
    
    print(f"🚢 Testing CrewAI Adapter with: {test_agent_path.name}\n")
    
    # Load manifest
    manifest = load_manifest(test_agent_path)
    print(f"✅ Loaded manifest: {manifest['name']}")
    print(f"   Context files: {len(manifest.get('required_context', []))}")
    
    # Generate agent config
    agent_config = generate_crewai_agent(test_agent_path)
    print(f"\n👤 CrewAI Agent Configuration:")
    print(f"   Role: {agent_config['role']}")
    print(f"   Goal: {agent_config['goal'][:80]}...")
    print(f"   Backstory: {agent_config['backstory'][:80]}...")
    print(f"   Tools: {len(agent_config['tools'])} tools")
    
    # Create agent wrapper
    print(f"\n🤖 Creating NoesisCrewAgent instance...")
    agent = NoesisCrewAgent(test_agent_path)
    print(f"   Agent role: {agent.get_role()}")
    print(f"   Agent goal: {agent.get_goal()[:60]}...")
    
    # Test crew creation
    print(f"\n⚙️  Creating Noesis Crew...")
    crew_config = create_noesis_crew([test_agent_path], ["Build a test feature"])
    print(f"   Crew agents: {len(crew_config['agents'])}")
    print(f"   Crew tasks: {len(crew_config['tasks'])}")
    print(f"   Process: {crew_config['process']}")
    
    print("\n✨ CrewAI adapter test complete!")


if __name__ == "__main__":
    test_crewai_adapter()
