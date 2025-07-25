"""
Orchestrator Agent - Routes user input to appropriate specialized agents
Acts as the main coordinator for the multi-agent system
"""

import os
from typing import Annotated
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.messages import SystemMessage

from .arithmetic_agent import create_arithmetic_agent, chat_with_arithmetic_agent
from .weather_agent import create_weather_agent, chat_with_weather_agent

class OrchestratorState(TypedDict):
    messages: Annotated[list, add_messages]

def create_orchestrator_agent():
    """Create the main orchestrator agent"""
    
    print("🎭 Creating Orchestrator Agent...")
    
    # Set up Google Gemini 1.5 Flash (back to basic)
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    
    if not gemini_api_key:
        raise Exception("No Gemini API key found!")
    
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        google_api_key=gemini_api_key,
        temperature=0.3
    )
    
    # Simple orchestrator system prompt
    ORCHESTRATOR_PROMPT = """You are an orchestrator agent that routes requests to specialized agents.

ROUTING RULES:
- For math/arithmetic questions: mention "ARITHMETIC" in your response
- For weather questions: mention "WEATHER" in your response  
- For general chat: respond directly

Examples:
- "Add 5 and 10" → "ARITHMETIC: I'll route this to the arithmetic agent"
- "Weather in London?" → "WEATHER: I'll check the weather for you"
- "Hello!" → "Hi! How can I help you today?"

Be clear about routing decisions."""

    # Create state graph
    graph_builder = StateGraph(OrchestratorState)
    
    def orchestrator_chatbot(state: OrchestratorState):
        messages = state["messages"].copy()
        
        # Add system prompt if not present
        has_system = any(getattr(msg, 'type', None) == 'system' for msg in messages)
        if not has_system:
            system_msg = SystemMessage(content=ORCHESTRATOR_PROMPT)
            messages = [system_msg] + messages
            
        response = llm.invoke(messages)
        return {"messages": [response]}
    
    # Add nodes
    graph_builder.add_node("orchestrator_chatbot", orchestrator_chatbot)
    
    # Add edges
    graph_builder.add_edge(START, "orchestrator_chatbot")
    graph_builder.add_edge("orchestrator_chatbot", END)
    
    # Compile
    graph = graph_builder.compile()
    
    print("✅ Orchestrator Agent ready!")
    return graph

class MultiAgentSystem:
    """Simplified multi-agent system"""
    
    def __init__(self):
        print("🚀 Initializing Multi-Agent System...")
        
        # Create all agents
        self.arithmetic_agent = create_arithmetic_agent()
        self.weather_agent = create_weather_agent()
        self.orchestrator = create_orchestrator_agent()
        
        print("🎉 Multi-Agent System ready!")
    
    async def chat(self, user_input: str):
        """Simple chat interface with basic routing"""
        print(f"\n🎭 [ORCHESTRATOR] Analyzing: {user_input}")
        
        # Get orchestrator decision
        result = self.orchestrator.invoke({"messages": [{"role": "user", "content": user_input}]})
        orchestrator_response = result["messages"][-1].content
        
        print(f"🎭 [ORCHESTRATOR] Decision: {orchestrator_response}")
        
        # Simple routing based on keywords in response
        if "ARITHMETIC" in orchestrator_response:
            print("📞 [ORCHESTRATOR] Routing to Arithmetic Agent...")
            return await chat_with_arithmetic_agent(self.arithmetic_agent, user_input)
        elif "WEATHER" in orchestrator_response:
            print("📞 [ORCHESTRATOR] Routing to Weather Agent...")
            return await chat_with_weather_agent(self.weather_agent, user_input)
        else:
            # Direct response from orchestrator
            print("💬 [ORCHESTRATOR] Direct response")
            return orchestrator_response

async def create_multi_agent_system():
    """Factory function to create the complete multi-agent system"""
    return MultiAgentSystem() 