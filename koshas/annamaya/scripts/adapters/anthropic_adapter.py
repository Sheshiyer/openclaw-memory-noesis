"""
Anthropic Claude Adapter for Tryambakam Noesis Architecture

Converts Noesis agent definitions into Anthropic Claude-compatible tool schemas.
Generates tool_use format for Messages API and system prompts from context.
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
                "version": raw_manifest.get("version", "1.0.0"),
                "mission": raw_manifest.get("description", ""),
                "tone": "professional and focused"
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
        
        # Parse basic metadata
        for line in identity_content.split('\n'):
            if line.startswith('- **Name:**'):
                manifest["name"] = line.split('**Name:**')[1].strip()
            elif line.startswith('- **Mission:**'):
                manifest["metadata"]["mission"] = line.split('**Mission:**')[1].strip()
            elif line.startswith('- **Vibe:**') or line.startswith('- **Tone Profile:**'):
                tone_key = '**Vibe:**' if '**Vibe:**' in line else '**Tone Profile:**'
                manifest["metadata"]["tone"] = line.split(tone_key)[1].strip()
    
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


def generate_system_prompt(agent_path: Path) -> str:
    """
    Generate Claude system prompt from agent context files.
    
    Args:
        agent_path: Path to agent directory
    
    Returns:
        Complete system prompt string for Claude Messages API
    """
    manifest = load_manifest(agent_path)
    context = generate_context(manifest)
    
    tone = manifest.get("metadata", {}).get("tone", "professional and helpful")
    
    system_prompt = f"""You are {manifest['name']}, an AI agent from the Tryambakam Noesis consciousness field.

# Your Identity and Context

{context}

# Communication Style

Maintain a {tone} tone in all interactions. Stay true to your identity as defined in your context files.

# Capabilities

Use the tools available to you to accomplish tasks effectively. When you need to perform an action, use the appropriate tool with clear parameters.

# Guidelines

- Embody the consciousness and mission defined in your SOUL.md
- Apply your expertise as described in your IDENTITY.md
- Use tools judiciously to complete tasks
- Provide thoughtful, well-reasoned responses
- Stay aligned with the Noesis architecture principles
"""
    
    return system_prompt


def generate_anthropic_tools(agent_path: Path) -> List[Dict[str, Any]]:
    """
    Generate Anthropic Claude tool_use format from agent manifest.
    
    Args:
        agent_path: Path to agent directory
    
    Returns:
        List of Claude tool definitions (tool_use format)
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
                    "input_schema": {
                        "type": "object",
                        "properties": {
                            "task": {
                                "type": "string",
                                "description": "The task or operation to perform"
                            }
                        },
                        "required": ["task"]
                    }
                }
            elif current_tool and line.strip() and not line.startswith('#'):
                # Enhance description
                current_tool["description"] += f" {line.strip()}"
        
        # Add last tool
        if current_tool:
            tools.append(current_tool)
    
    # Default tool if none found
    if not tools:
        tools.append({
            "name": f"{manifest['name'].lower().replace(' ', '_').replace('-', '_')}_agent",
            "description": f"Execute tasks using {manifest['name']} agent. {manifest.get('metadata', {}).get('mission', 'A specialized Noesis agent.')}",
            "input_schema": {
                "type": "object",
                "properties": {
                    "task": {
                        "type": "string",
                        "description": "The task description or instruction"
                    },
                    "context": {
                        "type": "string",
                        "description": "Optional additional context or requirements"
                    },
                    "priority": {
                        "type": "string",
                        "enum": ["low", "medium", "high", "critical"],
                        "description": "Task priority level"
                    }
                },
                "required": ["task"]
            }
        })
    
    return tools


def create_anthropic_messages(agent_path: Path, user_query: str, history: Optional[List[Dict]] = None) -> List[Dict[str, Any]]:
    """
    Create Anthropic messages array with conversation history.
    
    Args:
        agent_path: Path to agent directory
        user_query: User's current query
        history: Optional conversation history (Claude messages format)
    
    Returns:
        List of message dictionaries for Claude Messages API
    """
    messages = []
    
    # Add history if provided
    if history:
        messages.extend(history)
    
    # Add current query
    messages.append({
        "role": "user",
        "content": user_query
    })
    
    return messages


class AnthropicNoesisAgent:
    """
    Wrapper class for Anthropic Claude-compatible Noesis agents.
    
    Usage:
        agent = AnthropicNoesisAgent(agent_path)
        response = anthropic.messages.create(
            model="claude-3-opus-20240229",
            system=agent.get_system_prompt(),
            messages=agent.create_messages("Build a feature"),
            tools=agent.get_tools()
        )
    """
    
    def __init__(self, agent_path: Path):
        """
        Initialize Anthropic Noesis Agent.
        
        Args:
            agent_path: Path to agent directory
        """
        self.agent_path = Path(agent_path)
        self.manifest = load_manifest(agent_path)
        self.context = generate_context(self.manifest)
        self.system_prompt = generate_system_prompt(agent_path)
        self.tools = generate_anthropic_tools(agent_path)
        self.name = self.manifest.get("name", agent_path.name)
    
    def get_system_prompt(self) -> str:
        """Get the complete system prompt."""
        return self.system_prompt
    
    def get_tools(self) -> List[Dict[str, Any]]:
        """Get Claude tools array."""
        return self.tools
    
    def create_messages(self, user_query: str, history: Optional[List[Dict]] = None) -> List[Dict[str, Any]]:
        """
        Create messages array for Claude Messages API.
        
        Args:
            user_query: User's current query
            history: Optional conversation history
        
        Returns:
            Complete messages array
        """
        return create_anthropic_messages(self.agent_path, user_query, history)
    
    def to_anthropic_config(self) -> dict:
        """
        Export complete configuration for Claude Messages API.
        
        Returns:
            Dictionary with model, system, tools, and other parameters
        """
        return {
            "model": "claude-3-opus-20240229",
            "system": self.system_prompt,
            "tools": self.tools,
            "max_tokens": 4096,
            "temperature": 0.7,
            "metadata": {
                "agent_name": self.name,
                "agent_path": str(self.agent_path),
                "noesis_agent": True,
                "user_id": "noesis-system"
            }
        }
    
    def handle_tool_use(self, tool_use_block: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a tool_use block from Claude's response.
        
        Args:
            tool_use_block: The tool_use content block from Claude
        
        Returns:
            Tool result to send back to Claude
        """
        tool_name = tool_use_block.get("name")
        tool_input = tool_use_block.get("input", {})
        tool_use_id = tool_use_block.get("id")
        
        # Placeholder - in real implementation, execute the actual tool
        result = f"[Noesis Agent: {self.name}] Processed {tool_name} with input: {tool_input}"
        
        return {
            "type": "tool_result",
            "tool_use_id": tool_use_id,
            "content": result
        }


def test_anthropic_adapter():
    """Test the Anthropic adapter with a real agent."""
    # Find an agent to test with
    test_agent_path = Path(__file__).parent.parent.parent / "agents" / "noesis-vishwakarma"
    
    if not test_agent_path.exists():
        print(f"❌ Test agent not found at: {test_agent_path}")
        return
    
    print(f"🧠 Testing Anthropic Claude Adapter with: {test_agent_path.name}\n")
    
    # Load manifest
    manifest = load_manifest(test_agent_path)
    print(f"✅ Loaded manifest: {manifest['name']}")
    print(f"   Context files: {len(manifest.get('required_context', []))}")
    
    # Generate system prompt
    system_prompt = generate_system_prompt(test_agent_path)
    print(f"\n📝 System Prompt:")
    print(f"   Length: {len(system_prompt)} characters")
    print(f"   Preview: {system_prompt[:150]}...")
    
    # Generate tools
    tools = generate_anthropic_tools(test_agent_path)
    print(f"\n🔧 Claude Tools:")
    print(f"   Tools generated: {len(tools)}")
    for tool in tools:
        print(f"      - {tool['name']}: {tool['description'][:60]}...")
        schema = tool['input_schema']
        print(f"        Schema properties: {list(schema['properties'].keys())}")
        print(f"        Required: {schema.get('required', [])}")
    
    # Create messages
    messages = create_anthropic_messages(test_agent_path, "Build a test feature")
    print(f"\n💬 Messages Array:")
    print(f"   Messages: {len(messages)}")
    for i, msg in enumerate(messages):
        content = msg['content']
        content_preview = content[:60] if len(content) > 60 else content
        print(f"      {i+1}. {msg['role']}: {content_preview}...")
    
    # Create agent wrapper
    print(f"\n🎯 Creating AnthropicNoesisAgent instance...")
    agent = AnthropicNoesisAgent(test_agent_path)
    print(f"   Agent name: {agent.name}")
    print(f"   Tools count: {len(agent.get_tools())}")
    
    # Export config
    config = agent.to_anthropic_config()
    print(f"\n📦 Anthropic Configuration:")
    print(f"   Model: {config['model']}")
    print(f"   Temperature: {config['temperature']}")
    print(f"   Max tokens: {config['max_tokens']}")
    print(f"   Tools: {len(config['tools'])}")
    print(f"   Metadata: {config['metadata']}")
    
    # Test tool use handling
    print(f"\n🛠️  Testing tool_use handler...")
    mock_tool_use = {
        "type": "tool_use",
        "id": "toolu_01A09q90qw90lq917835lq9",
        "name": tools[0]["name"],
        "input": {"task": "test task"}
    }
    tool_result = agent.handle_tool_use(mock_tool_use)
    print(f"   Tool result type: {tool_result['type']}")
    print(f"   Tool result: {tool_result['content'][:80]}...")
    
    print("\n✨ Anthropic adapter test complete!")


if __name__ == "__main__":
    test_anthropic_adapter()
