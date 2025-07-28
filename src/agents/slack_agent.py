"""
Slack Agent - Specialized for sending messages to Slack channels
Handles Slack webhook messaging with channel validation
"""

import os
from typing import Annotated
from langchain_google_genai import ChatGoogleGenerativeAI
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.messages import SystemMessage

# Import the Slack messaging tool
from ..tools import send_slack_message, SLACK_CHANNELS

class SlackState(TypedDict):
    messages: Annotated[list, add_messages]

def create_slack_agent():
    """Create a specialized Slack messaging agent"""
    
    print("📱 Creating Slack Agent...")
    
    # Set up Google Gemini 2.0 Flash
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    
    if not gemini_api_key:
        raise Exception("No Gemini API key found!")
    
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        google_api_key=gemini_api_key,
        temperature=0.2  # Lower temperature for precise messaging
    )
    
    # Slack-specific tools
    slack_tools = [send_slack_message]
    llm_with_tools = llm.bind_tools(slack_tools)
    
    # Get available channels for the prompt
    available_channels = ", ".join(SLACK_CHANNELS.keys())
    
    # Slack-specific system prompt
    SLACK_PROMPT = f"""You are a specialized Slack messaging agent. Your expertise is sending messages to Slack channels.

📱 YOUR ROLE:
- You ONLY handle Slack messaging requests
- Use send_slack_message tool to send messages to authorized channels
- Always validate channel permissions before sending
- Provide clear feedback on message delivery status

📋 AVAILABLE CHANNELS: {available_channels}

🎯 EXAMPLES:
- "Send 'Hello team' to general" → Use send_slack_message tool with channel='general'
- "Post update to development channel" → Use send_slack_message tool with channel='development'
- "Send message to random-channel" → Will return permission error

⚠️ IMPORTANT:
- Only send messages to authorized channels: {available_channels}
- For unauthorized channels, inform user about permission restrictions
- Always confirm successful message delivery"""

    # Create state graph
    graph_builder = StateGraph(SlackState)
    
    def slack_chatbot(state: SlackState):
        messages = state["messages"].copy()
        
        # Add Slack system prompt
        has_system = any(getattr(msg, 'type', None) == 'system' for msg in messages)
        if not has_system:
            system_msg = SystemMessage(content=SLACK_PROMPT)
            messages = [system_msg] + messages
            
        return {"messages": [llm_with_tools.invoke(messages)]}
    
    # Add nodes
    graph_builder.add_node("slack_chatbot", slack_chatbot)
    
    tool_node = ToolNode(tools=slack_tools)
    graph_builder.add_node("slack_tools", tool_node)
    
    # Add edges
    graph_builder.add_edge(START, "slack_chatbot")
    graph_builder.add_conditional_edges(
        "slack_chatbot",
        tools_condition,
        {"tools": "slack_tools", "__end__": END}
    )
    graph_builder.add_edge("slack_tools", "slack_chatbot")
    
    # Compile
    graph = graph_builder.compile()
    
    print("✅ Slack Agent ready!")
    print(f"📋 Available channels: {available_channels}")
    return graph
