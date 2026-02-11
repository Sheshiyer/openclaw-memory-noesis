"""
OpenAI Adapter for Tryambakam Noesis Architecture

Converts Noesis agent definitions into OpenAI-compatible function calling schemas.
Generates tools format for ChatCompletion API and system prompts from context.
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
                "mission": raw_manifest.get("description", "")
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
            elif line.startswith('- **Vibe:**'):
                manifest["metadata"]["vibe"] = line.split('**Vibe:**')[1].strip()
    
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
    Generate OpenAI system prompt from agent context files.
    
    Args:
        agent_path: Path to agent directory
    
    Returns:
        Complete system prompt string for OpenAI ChatCompletion
    """
    manifest = load_manifest(agent_path)
    context = generate_context(manifest)
    
    system_prompt = f"""You are {manifest['name']}, an AI agent from the Tryambakam Noesis consciousness field.

# Your Context and Identity

{context}

# Instructions

- Stay in character based on your SOUL.md and IDENTITY.md context
- Use your capabilities and tools to accomplish tasks
- Provide clear, actionable responses
- Call functions when appropriate to complete tasks
"""
    
    return system_prompt


def generate_openai_functions(agent_path: Path) -> List[Dict[str, Any]]:
    """
    Generate OpenAI function calling schema from agent manifest.
    
    Args:
        agent_path: Path to agent directory
    
    Returns:
        List of OpenAI function definitions (tools format)
    """
    manifest = load_manifest(agent_path)
    functions = []
    
    # Read TOOLS.md if available
    tools_file = Path(agent_path) / "TOOLS.md"
    if tools_file.exists():
        tools_content = tools_file.read_text()
        
        # Parse tools from markdown
        current_func = None
        for line in tools_content.split('\n'):
            if line.startswith('##') or line.startswith('###'):
                # Save previous function
                if current_func:
                    functions.append(current_func)
                
                # Start new function
                func_name = line.lstrip('#').strip()
                current_func = {
                    "type": "function",
                    "function": {
                        "name": func_name.lower().replace(' ', '_').replace('-', '_'),
                        "description": func_name,
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "task": {
                                    "type": "string",
                                    "description": "The task or query to process"
                                }
                            },
                            "required": ["task"]
                        }
                    }
                }
            elif current_func and line.strip() and not line.startswith('#'):
                # Add to description
                current_func["function"]["description"] += f" {line.strip()}"
        
        # Add last function
        if current_func:
            functions.append(current_func)
    
    # Default function if none found
    if not functions:
        functions.append({
            "type": "function",
            "function": {
                "name": f"{manifest['name'].lower().replace(' ', '_').replace('-', '_')}_execute",
                "description": f"Execute a task using {manifest['name']} agent capabilities. {manifest.get('metadata', {}).get('mission', '')}",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "task": {
                            "type": "string",
                            "description": "The task description or query"
                        },
                        "context": {
                            "type": "string",
                            "description": "Optional additional context for the task"
                        }
                    },
                    "required": ["task"]
                }
            }
        })
    
    return functions


def create_openai_messages(agent_path: Path, user_query: str) -> List[Dict[str, str]]:
    """
    Create OpenAI messages array with system prompt and user query.
    
    Args:
        agent_path: Path to agent directory
        user_query: User's query or task
    
    Returns:
        List of message dictionaries for OpenAI ChatCompletion
    """
    system_prompt = generate_system_prompt(agent_path)
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_query}
    ]
    
    return messages


class OpenAINoesisAgent:
    """
    Wrapper class for OpenAI-compatible Noesis agents.
    
    Usage:
        agent = OpenAINoesisAgent(agent_path)
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=agent.create_messages("Build a feature"),
            tools=agent.get_tools()
        )
    """
    
    def __init__(self, agent_path: Path):
        """
        Initialize OpenAI Noesis Agent.
        
        Args:
            agent_path: Path to agent directory
        """
        self.agent_path = Path(agent_path)
        self.manifest = load_manifest(agent_path)
        self.context = generate_context(self.manifest)
        self.system_prompt = generate_system_prompt(agent_path)
        self.functions = generate_openai_functions(agent_path)
        self.name = self.manifest.get("name", agent_path.name)
    
    def get_system_prompt(self) -> str:
        """Get the complete system prompt."""
        return self.system_prompt
    
    def get_tools(self) -> List[Dict[str, Any]]:
        """Get OpenAI tools/functions array."""
        return self.functions
    
    def create_messages(self, user_query: str, history: Optional[List[Dict]] = None) -> List[Dict[str, str]]:
        """
        Create messages array for OpenAI ChatCompletion.
        
        Args:
            user_query: User's current query
            history: Optional conversation history
        
        Returns:
            Complete messages array
        """
        messages = [{"role": "system", "content": self.system_prompt}]
        
        # Add history if provided
        if history:
            messages.extend(history)
        
        # Add current query
        messages.append({"role": "user", "content": user_query})
        
        return messages
    
    def to_openai_config(self) -> dict:
        """
        Export complete configuration for OpenAI ChatCompletion.
        
        Returns:
            Dictionary with model, messages, tools, and other parameters
        """
        return {
            "model": "gpt-4-turbo-preview",
            "messages": [{"role": "system", "content": self.system_prompt}],
            "tools": self.functions,
            "tool_choice": "auto",
            "temperature": 0.7,
            "max_tokens": 4096,
            "metadata": {
                "agent_name": self.name,
                "agent_path": str(self.agent_path),
                "noesis_agent": True
            }
        }


def test_openai_adapter():
    """Test the OpenAI adapter with a real agent."""
    # Find an agent to test with
    test_agent_path = Path(__file__).parent.parent.parent / "agents" / "noesis-vishwakarma"
    
    if not test_agent_path.exists():
        print(f"❌ Test agent not found at: {test_agent_path}")
        return
    
    print(f"🤖 Testing OpenAI Adapter with: {test_agent_path.name}\n")
    
    # Load manifest
    manifest = load_manifest(test_agent_path)
    print(f"✅ Loaded manifest: {manifest['name']}")
    print(f"   Context files: {len(manifest.get('required_context', []))}")
    
    # Generate system prompt
    system_prompt = generate_system_prompt(test_agent_path)
    print(f"\n📝 System Prompt:")
    print(f"   Length: {len(system_prompt)} characters")
    print(f"   Preview: {system_prompt[:150]}...")
    
    # Generate functions
    functions = generate_openai_functions(test_agent_path)
    print(f"\n🔧 OpenAI Functions:")
    print(f"   Functions generated: {len(functions)}")
    for func in functions:
        func_def = func["function"]
        print(f"      - {func_def['name']}: {func_def['description'][:60]}...")
        print(f"        Parameters: {list(func_def['parameters']['properties'].keys())}")
    
    # Create messages
    messages = create_openai_messages(test_agent_path, "Build a test feature")
    print(f"\n💬 Messages Array:")
    print(f"   Messages: {len(messages)}")
    for i, msg in enumerate(messages):
        content_preview = msg['content'][:60] if len(msg['content']) > 60 else msg['content']
        print(f"      {i+1}. {msg['role']}: {content_preview}...")
    
    # Create agent wrapper
    print(f"\n🎯 Creating OpenAINoesisAgent instance...")
    agent = OpenAINoesisAgent(test_agent_path)
    print(f"   Agent name: {agent.name}")
    print(f"   Tools count: {len(agent.get_tools())}")
    
    # Export config
    config = agent.to_openai_config()
    print(f"\n📦 OpenAI Configuration:")
    print(f"   Model: {config['model']}")
    print(f"   Temperature: {config['temperature']}")
    print(f"   Tool choice: {config['tool_choice']}")
    print(f"   Max tokens: {config['max_tokens']}")
    
    print("\n✨ OpenAI adapter test complete!")


if __name__ == "__main__":
    test_openai_adapter()
