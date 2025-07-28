"""
Orchestrator V2 - Simplified Workflow Orchestrator (Beginner-Friendly)
Demonstrates tool-based agent execution with workflow state, but simplified
"""

import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.messages import SystemMessage

from .arithmetic_agent import create_arithmetic_agent
from .weather_agent import create_weather_agent
from .slack_agent import create_slack_agent

# Import states and tools from separate modules
from ..states import SimpleWorkflowState
from ..tools import create_orchestrator_tools

class SimpleOrchestratorV2:
    """Simplified V2 Orchestrator - Easy to understand but keeps V2 concepts"""
    
    def __init__(self):
        print("🎭 Creating Simple Orchestrator V2...")
        
        # Hardcoded agents - much simpler!
        print("🔧 Setting up agents directly...")
        self.arithmetic_agent = create_arithmetic_agent()
        self.weather_agent = create_weather_agent()
        self.slack_agent = create_slack_agent()
        
        # Create LLM
        gemini_api_key = os.getenv("GEMINI_API_KEY")
        if not gemini_api_key:
            raise Exception("No Gemini API key found!")
        
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",  # Using 1.5 flash to avoid quota issues
            google_api_key=gemini_api_key,
            temperature=0.2
        )
        
        # Create tools that actually execute agents (V2 concept)
        self.tools = create_orchestrator_tools(self.arithmetic_agent, self.weather_agent, self.slack_agent)
        self.llm_with_tools = self.llm.bind_tools(self.tools)
        
        # Create workflow graph
        self.workflow_graph = self._create_workflow()
        
        print("✅ Simple Orchestrator V2 ready!")
    

    
    def _create_workflow(self):
        """Create the workflow graph - simpler than complex V2"""
        
        # Simple but intelligent system prompt
        SYSTEM_PROMPT = """You are a V2 orchestrator that executes agents using tools. 

🔧 AVAILABLE TOOLS:
- execute_math_agent: For math/arithmetic questions
- execute_weather_agent: For weather questions
- execute_slack_agent: For sending messages to Slack channels

🎯 YOUR JOB:
1. Analyze the user's question
2. Use the appropriate tool to execute the right agent
3. For complex questions, you can use multiple tools in sequence
4. Pass context between tools when needed

EXAMPLES:
- "Add 5 and 10" → Use execute_math_agent
- "Weather in London?" → Use execute_weather_agent  
- "Send 'Hello team' to general channel" → Use execute_slack_agent

Be smart about using tools and passing context!"""

        graph_builder = StateGraph(SimpleWorkflowState)
        
        def orchestrator_with_tools(state: SimpleWorkflowState):
            """Main orchestrator node with tool capabilities"""
            messages = state["messages"].copy()
            
            # Add system prompt
            has_system = any(getattr(msg, 'type', None) == 'system' for msg in messages)
            if not has_system:
                system_msg = SystemMessage(content=SYSTEM_PROMPT)
                messages = [system_msg] + messages
            
            # Add context from previous agent results if available
            if state.get("context"):
                context_info = f"\nPrevious context: {state['context']}"
                if messages and hasattr(messages[-1], 'content'):
                    messages[-1].content += context_info
            
            response = self.llm_with_tools.invoke(messages)
            return {"messages": [response]}
        
        def update_context(state: SimpleWorkflowState):
            """Update context with agent results - simple V2 feature"""
            messages = state["messages"]
            agent_results = state.get("agent_results", {})
            
            # Simple context building from the last message
            if messages:
                last_content = getattr(messages[-1], 'content', '')
                new_context = f"Latest result: {last_content}"
                
                return {
                    "context": new_context,
                    "agent_results": {**agent_results, f"step_{len(agent_results)}": last_content}
                }
            
            return {"context": state.get("context", "")}
        
        # Add nodes
        graph_builder.add_node("orchestrator_with_tools", orchestrator_with_tools)
        graph_builder.add_node("tool_execution", ToolNode(tools=self.tools))
        graph_builder.add_node("update_context", update_context)
        
        # Add edges - this creates the V2 workflow
        graph_builder.add_edge(START, "orchestrator_with_tools")
        graph_builder.add_conditional_edges(
            "orchestrator_with_tools",
            tools_condition,
            {"tools": "tool_execution", "__end__": "update_context"}
        )
        graph_builder.add_edge("tool_execution", "update_context")
        graph_builder.add_edge("update_context", END)
        
        return graph_builder.compile()
    
    async def chat(self, user_input: str) -> str:
        """Simple chat interface for V2 orchestrator"""
        print(f"\n🎭 [V2 ORCHESTRATOR] Starting: {user_input}")
        
        # Initialize simple workflow state
        initial_state = {
            "messages": [{"role": "user", "content": user_input}],
            "agent_results": {},
            "context": ""
        }
        
        try:
            # Execute the V2 workflow
            result = self.workflow_graph.invoke(initial_state)
            
            # Extract response
            final_message = result["messages"][-1]
            response = final_message.content if hasattr(final_message, 'content') else str(final_message)
            
            # Show what agents were executed
            agent_results = result.get("agent_results", {})
            if agent_results:
                print(f"🎭 [V2 ORCHESTRATOR] Agent results: {agent_results}")
            
            return response
            
        except Exception as e:
            error_msg = f"V2 Orchestrator failed: {str(e)}"
            print(f"❌ {error_msg}")
            return f"Sorry, I encountered an error: {error_msg}"

# Factory function
async def create_simple_orchestrator_v2():
    """Create the simplified V2 orchestrator"""
    return SimpleOrchestratorV2() 