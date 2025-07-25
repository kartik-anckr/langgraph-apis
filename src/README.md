# 🐍 Python LangGraph Agent

This is the **Python implementation** of the LangGraph agent using Google Gemini 1.5 Flash.

## 📁 **Structure**

```
src/
├── __init__.py           # Package initialization
├── basic_agent.py        # Core LangGraph agent
├── main.py              # FastAPI server
└── utils/
    └── __init__.py      # Utility functions package
```

## 🚀 **Quick Start**

### 1. Install Dependencies

```bash
# From the root directory
pip3 install -r requirements.txt
```

### 2. Environment Setup

Make sure you have `.env` file in the root directory with:

```
GEMINI_API_KEY=your_actual_gemini_api_key_here
```

### 3. Run Options

**Test the Agent Directly:**

```bash
python3 -m src.basic_agent
# OR (from root directory)
cd src && python3 basic_agent.py
```

**Start the FastAPI Server:**

```bash
python3 -m src.main
# OR (from root directory)
cd src && python3 main.py
```

## 🎯 **What Each File Does**

### `basic_agent.py`

- Core LangGraph agent implementation
- Uses Google Gemini 1.5 Flash LLM
- Includes addition tool that LLM can call automatically
- Follows official LangGraph patterns from documentation

### `main.py`

- FastAPI server (like Express.js for Python)
- Provides REST endpoints:
  - `GET /` - Welcome message
  - `GET /health` - System status
  - `POST /chat` - Chat with the agent
  - `GET /docs` - Auto-generated API documentation

### `__init__.py`

- Makes `src` a Python package
- Exports main functions for easy importing

### `utils/`

- Package for utility functions (expandable)

## 🧪 **Testing the Agent**

**Direct Agent Test:**

```bash
python3 -m src.basic_agent
```

**FastAPI Server Test:**

```bash
# Start server
python3 -m src.main

# Visit in browser:
# http://localhost:8000 - API info
# http://localhost:8000/docs - Interactive API docs

# Or test with curl:
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Can you add 15 and 25?"}'
```

## 🌟 **Features**

✅ **Automatic Tool Selection** - LLM decides when to use tools  
✅ **Addition Tool** - Can perform math calculations  
✅ **Smart Routing** - Math questions use tools, chat doesn't  
✅ **FastAPI Server** - RESTful API with auto-docs  
✅ **Google Gemini 1.5 Flash** - Fast and efficient AI model  
✅ **Type Hints** - Full Python type annotations

## 📊 **Example Usage**

```python
from src import create_agent, chat_with_agent

agent = create_agent()

# Math question - uses addition tool automatically
await chat_with_agent(agent, "What is 10 + 20?")
# Output: Tool used: 10 + 20 = 30

# Regular chat - no tools needed
await chat_with_agent(agent, "Hello! How are you?")
# Output: Direct AI response
```

## 🔗 **Compare with JavaScript**

See the main project `Python_vs_JavaScript_Comparison.md` for detailed comparison between this Python implementation and the JavaScript version.

## 📚 **Learning Resources**

- [LangGraph Official Docs](https://langchain-ai.github.io/langgraph/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Google Gemini API](https://ai.google.dev/)
