"""
Tools module - exports all available tools
"""

import importlib.util
import os

# Import slack tools from the slack.tools directory
_slack_tools_path = os.path.join(os.path.dirname(__file__), 'slack.tools', 'slack_messaging.py')
_spec = importlib.util.spec_from_file_location("slack_messaging", _slack_tools_path)
_slack_messaging = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_slack_messaging)

# Export the slack tools
send_slack_message = _slack_messaging.send_slack_message
SLACK_CHANNELS = _slack_messaging.SLACK_CHANNELS

# Import orchestrator tools from orchestrator.tools directory
import sys
_tools_dir = os.path.join(os.path.dirname(__file__), 'orchestrator.tools')
sys.path.insert(0, _tools_dir)
try:
    from math_agent_tool import create_math_agent_tool
    from weather_agent_tool import create_weather_agent_tool
    from slack_agent_tool import create_slack_agent_tool
    
    def create_orchestrator_tools(arithmetic_agent, weather_agent, slack_agent):
        """Create all orchestrator tools"""
        
        math_tool = create_math_agent_tool(arithmetic_agent)
        weather_tool = create_weather_agent_tool(weather_agent)
        slack_tool = create_slack_agent_tool(slack_agent)
        
        return [math_tool, weather_tool, slack_tool]
finally:
    sys.path.remove(_tools_dir)

__all__ = ['send_slack_message', 'SLACK_CHANNELS', 'create_orchestrator_tools'] 