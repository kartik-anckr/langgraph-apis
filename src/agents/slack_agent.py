"""
Slack Agent - Specialized for sending messages to Slack channels
Handles Slack webhook messaging with channel validation
"""

import os
import json
import requests
from typing import Annotated
from langchain_google_genai import ChatGoogleGenerativeAI
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.messages import SystemMessage
from langchain_core.tools import tool

# Predefined Slack channels with their webhook URLs
SLACK_CHANNELS = {
    "team": "https://hooks.slack.com/services/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",
    "development": "https://hooks.slack.com/services/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", 
}

@tool
def send_slack_message(channel: str, message: str) -> str:
    """
    Send a message to a Slack channel via webhook
    
    Args:
        channel: The Slack channel name (e.g., 'general', 'development')
        message: The message to send
    
    Returns:
        Success/failure message
    """
    print(f"🔔 [SLACK TOOL] Attempting to send message to #{channel}")
    
    # Check if channel exists in our allowed channels
    if channel not in SLACK_CHANNELS:
        available_channels = ", ".join(SLACK_CHANNELS.keys())
        error_msg = f"❌ I don't have permission to send messages to #{channel}. Available channels: {available_channels}"
        print(f"🔔 [SLACK TOOL] {error_msg}")
        return error_msg
    
    # Get webhook URL for the channel
    webhook_url = SLACK_CHANNELS[channel]
    
    # Prepare Slack message payload
    payload = {
        "text": message,
        "channel": f"#{channel}",
        "username": "Assistant Bot",
        "icon_emoji": ":robot_face:"
    }
    
    try:
        # Send POST request to Slack webhook
        response = requests.post(
            webhook_url,
            data=json.dumps(payload),
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        if response.status_code == 200:
            success_msg = f"✅ Message sent successfully to #{channel}"
            print(f"🔔 [SLACK TOOL] {success_msg}")
            return success_msg
        else:
            error_msg = f"❌ Failed to send message to #{channel}. Status code: {response.status_code}"
            print(f"🔔 [SLACK TOOL] {error_msg}")
            return error_msg
            
    except requests.exceptions.RequestException as e:
        error_msg = f"❌ Network error sending message to #{channel}: {str(e)}"
        print(f"🔔 [SLACK TOOL] {error_msg}")
        return error_msg
    except Exception as e:
        error_msg = f"❌ Unexpected error sending message to #{channel}: {str(e)}"
        print(f"🔔 [SLACK TOOL] {error_msg}")
        return error_msg

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

async def chat_with_slack_agent(agent, user_input: str):
    """Chat with the Slack agent"""
    print(f"📱 [SLACK AGENT] Processing: {user_input}")
    
    result = agent.invoke({"messages": [{"role": "user", "content": user_input}]})
    response = result["messages"][-1].content
    
    print(f"📱 [SLACK AGENT] Result: {response}")
    return response 