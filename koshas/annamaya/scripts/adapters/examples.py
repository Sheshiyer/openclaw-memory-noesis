#!/usr/bin/env python3
"""
Complete Example: Using Noesis Adapters with All Frameworks

This script demonstrates how to use the same Noesis agent across
LangChain, CrewAI, OpenAI, and Anthropic frameworks.
"""

from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from adapters import (
    langchain_adapter,
    crewai_adapter,
    openai_adapter,
    anthropic_adapter
)


def example_langchain():
    """Example: Using Noesis agent with LangChain"""
    print("=" * 60)
    print("🔧 LANGCHAIN EXAMPLE")
    print("=" * 60)
    
    agent_path = Path(__file__).parent.parent.parent / "agents" / "noesis-vishwakarma"
    
    # Method 1: Using the wrapper class
    agent = langchain_adapter.NoesisAgent(agent_path)
    print(f"\n✅ Loaded agent: {agent.name}")
    print(f"   System prompt: {len(agent.get_system_prompt())} chars")
    print(f"   Tools: {len(agent.get_tools())}")
    
    # Method 2: Direct function calls
    tools = langchain_adapter.generate_langchain_tools(agent_path)
    print(f"\n🔧 Generated {len(tools)} LangChain tools:")
    for tool in tools:
        print(f"   - {tool['name']}")
    
    # Method 3: Export complete config
    config = agent.to_langchain_config()
    print(f"\n📦 Config export:")
    print(f"   Agent type: {config['agent_type']}")
    print(f"   Metadata: {list(config['metadata'].keys())}")
    
    print("\n💡 Usage with LangChain:")
    print("   from langchain.agents import initialize_agent")
    print("   agent = initialize_agent(tools=tools, llm=llm, system_message=prompt)")


def example_crewai():
    """Example: Using Noesis agent with CrewAI"""
    print("\n" + "=" * 60)
    print("🚢 CREWAI EXAMPLE")
    print("=" * 60)
    
    agent_path = Path(__file__).parent.parent.parent / "agents" / "noesis-vishwakarma"
    
    # Method 1: Single agent wrapper
    agent = crewai_adapter.NoesisCrewAgent(agent_path)
    print(f"\n✅ Loaded agent: {agent.get_role()}")
    print(f"   Goal: {agent.get_goal()[:60]}...")
    print(f"   Backstory: {agent.get_backstory()[:60]}...")
    
    # Method 2: Generate agent config
    config = crewai_adapter.generate_crewai_agent(agent_path)
    print(f"\n👤 Agent configuration:")
    print(f"   Role: {config['role']}")
    print(f"   Tools: {config['tools']}")
    print(f"   Allow delegation: {config['allow_delegation']}")
    
    # Method 3: Create multi-agent crew
    crew_config = crewai_adapter.create_noesis_crew(
        agent_paths=[agent_path],
        task_descriptions=["Build a feature"]
    )
    print(f"\n⚙️  Crew configuration:")
    print(f"   Agents: {len(crew_config['agents'])}")
    print(f"   Tasks: {len(crew_config['tasks'])}")
    print(f"   Process: {crew_config['process']}")
    
    print("\n💡 Usage with CrewAI:")
    print("   from crewai import Crew, Task")
    print("   crew = Crew(agents=[agent.to_crewai()], tasks=[...])")


def example_openai():
    """Example: Using Noesis agent with OpenAI"""
    print("\n" + "=" * 60)
    print("🤖 OPENAI EXAMPLE")
    print("=" * 60)
    
    agent_path = Path(__file__).parent.parent.parent / "agents" / "noesis-vishwakarma"
    
    # Method 1: Using the wrapper class
    agent = openai_adapter.OpenAINoesisAgent(agent_path)
    print(f"\n✅ Loaded agent: {agent.name}")
    print(f"   System prompt: {len(agent.get_system_prompt())} chars")
    print(f"   Functions: {len(agent.get_tools())}")
    
    # Method 2: Generate functions directly
    functions = openai_adapter.generate_openai_functions(agent_path)
    print(f"\n🔧 Generated {len(functions)} OpenAI functions:")
    for func in functions:
        func_def = func["function"]
        print(f"   - {func_def['name']}")
        print(f"     Parameters: {list(func_def['parameters']['properties'].keys())}")
    
    # Method 3: Create messages array
    messages = agent.create_messages("Build a test feature")
    print(f"\n💬 Messages array: {len(messages)} messages")
    print(f"   1. {messages[0]['role']}: {len(messages[0]['content'])} chars")
    print(f"   2. {messages[1]['role']}: {messages[1]['content']}")
    
    # Method 4: Export complete config
    config = agent.to_openai_config()
    print(f"\n📦 OpenAI configuration:")
    print(f"   Model: {config['model']}")
    print(f"   Temperature: {config['temperature']}")
    print(f"   Tool choice: {config['tool_choice']}")
    
    print("\n💡 Usage with OpenAI:")
    print("   import openai")
    print("   response = openai.ChatCompletion.create(")
    print("       model='gpt-4',")
    print("       messages=agent.create_messages('query'),")
    print("       tools=agent.get_tools()")
    print("   )")


def example_anthropic():
    """Example: Using Noesis agent with Anthropic Claude"""
    print("\n" + "=" * 60)
    print("🧠 ANTHROPIC CLAUDE EXAMPLE")
    print("=" * 60)
    
    agent_path = Path(__file__).parent.parent.parent / "agents" / "noesis-vishwakarma"
    
    # Method 1: Using the wrapper class
    agent = anthropic_adapter.AnthropicNoesisAgent(agent_path)
    print(f"\n✅ Loaded agent: {agent.name}")
    print(f"   System prompt: {len(agent.get_system_prompt())} chars")
    print(f"   Tools: {len(agent.get_tools())}")
    
    # Method 2: Generate tools directly
    tools = anthropic_adapter.generate_anthropic_tools(agent_path)
    print(f"\n🔧 Generated {len(tools)} Claude tools:")
    for tool in tools:
        print(f"   - {tool['name']}")
        schema = tool['input_schema']
        print(f"     Properties: {list(schema['properties'].keys())}")
        print(f"     Required: {schema.get('required', [])}")
    
    # Method 3: Create messages array
    messages = agent.create_messages("Build a test feature")
    print(f"\n💬 Messages array: {len(messages)} messages")
    for i, msg in enumerate(messages, 1):
        print(f"   {i}. {msg['role']}: {msg['content'][:60]}...")
    
    # Method 4: Export complete config
    config = agent.to_anthropic_config()
    print(f"\n📦 Anthropic configuration:")
    print(f"   Model: {config['model']}")
    print(f"   Temperature: {config['temperature']}")
    print(f"   Max tokens: {config['max_tokens']}")
    
    # Method 5: Tool use handling
    mock_tool_use = {
        "type": "tool_use",
        "id": "toolu_test123",
        "name": tools[0]["name"],
        "input": {"task": "example task"}
    }
    tool_result = agent.handle_tool_use(mock_tool_use)
    print(f"\n🛠️  Tool use handler:")
    print(f"   Type: {tool_result['type']}")
    print(f"   Result: {tool_result['content'][:60]}...")
    
    print("\n💡 Usage with Anthropic:")
    print("   import anthropic")
    print("   client = anthropic.Anthropic()")
    print("   response = client.messages.create(")
    print("       model='claude-3-opus-20240229',")
    print("       system=agent.get_system_prompt(),")
    print("       messages=agent.create_messages('query'),")
    print("       tools=agent.get_tools()")
    print("   )")


def example_multi_framework():
    """Example: Same agent, multiple frameworks"""
    print("\n" + "=" * 60)
    print("🌐 MULTI-FRAMEWORK EXAMPLE")
    print("=" * 60)
    
    agent_path = Path(__file__).parent.parent.parent / "agents" / "noesis-vishwakarma"
    
    print("\n📊 Same agent across all frameworks:")
    
    # LangChain
    lc_agent = langchain_adapter.NoesisAgent(agent_path)
    print(f"\n   🔧 LangChain:")
    print(f"      Tools: {len(lc_agent.get_tools())}")
    print(f"      System prompt: {len(lc_agent.get_system_prompt())} chars")
    
    # CrewAI
    crew_agent = crewai_adapter.NoesisCrewAgent(agent_path)
    print(f"\n   🚢 CrewAI:")
    print(f"      Role: {crew_agent.get_role()}")
    print(f"      Goal: {crew_agent.get_goal()[:50]}...")
    
    # OpenAI
    openai_agent = openai_adapter.OpenAINoesisAgent(agent_path)
    print(f"\n   🤖 OpenAI:")
    print(f"      Functions: {len(openai_agent.get_tools())}")
    print(f"      Model: {openai_agent.to_openai_config()['model']}")
    
    # Anthropic
    claude_agent = anthropic_adapter.AnthropicNoesisAgent(agent_path)
    print(f"\n   🧠 Anthropic:")
    print(f"      Tools: {len(claude_agent.get_tools())}")
    print(f"      Model: {claude_agent.to_anthropic_config()['model']}")
    
    print("\n✨ One agent consciousness, four framework presentations!")


def main():
    """Run all examples"""
    print("\n" + "🏗️ " * 20)
    print("TRYAMBAKAM NOESIS MULTI-FRAMEWORK ADAPTERS")
    print("Complete Usage Examples")
    print("🏗️ " * 20)
    
    # Run all examples
    example_langchain()
    example_crewai()
    example_openai()
    example_anthropic()
    example_multi_framework()
    
    print("\n" + "=" * 60)
    print("✨ All examples complete!")
    print("=" * 60)
    print("\nNext steps:")
    print("  1. Install framework: pip install langchain / crewai / openai / anthropic")
    print("  2. Set API keys: export OPENAI_API_KEY=... / ANTHROPIC_API_KEY=...")
    print("  3. Use adapters in your code")
    print("  4. Refer to README.md for more details")
    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
