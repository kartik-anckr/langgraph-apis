# 🤖 LangGraph Beginner Project with Google Gemini 1.5 Flash

A **super simple** LangGraph project for beginners with both **Python** and **JavaScript** implementations using **Google Gemini 1.5 Flash** AI model.

## 🎯 **What is this project?**

This project shows you how to build the **exact same AI agent** in both Python and JavaScript:

- Use **LangGraph** (simple way to build AI workflows)
- Connect to **Google Gemini 1.5 Flash** (fast and free AI model)
- Create API servers (**FastAPI** for Python, **Express.js** for JavaScript)
- Follow **official LangGraph patterns** with automatic tool selection

## 📁 **Project Structure**

```
langgraph/
├── README.md                           # This file
├── .env                               # Your API keys
├── .env.example                       # Template for .env
├── requirements.txt                   # Python dependencies
├── setup.py                          # Python automated setup
├── tutorial.md                       # Detailed learning guide
├── Python_vs_JavaScript_Comparison.md # Side-by-side comparison
├── src/                              # 🐍 Python Implementation
│   ├── __init__.py                   # Package initialization
│   ├── basic_agent.py                # Core LangGraph agent
│   ├── main.py                       # FastAPI server
│   ├── README.md                     # Python-specific docs
│   └── utils/
│       └── __init__.py
└── js/                               # 🟨 JavaScript Implementation
    ├── package.json                  # Dependencies and scripts
    ├── README.md                     # JavaScript-specific docs
    └── src/
        ├── basic_agent.js            # Core LangGraph agent
        └── main.js                   # Express.js server
```

## 🚀 **Quick Start**

### 1. Get your free Gemini API key

- Visit: https://ai.google.dev/
- Create a `.env` file in the root:

```
GEMINI_API_KEY=your_actual_api_key_here
```

### 2. Choose your language:

#### 🐍 **Python** (Recommended for beginners)

```bash
# Install dependencies
pip3 install -r requirements.txt

# Test the agent
python3 -m src.basic_agent

# Start API server
python3 -m src.main
```

#### 🟨 **JavaScript**

```bash
# Install dependencies
cd js && npm install

# Test the agent
npm run agent

# Start API server
npm start
```

## 🎯 **What Both Implementations Do**

✅ **Smart Tool Selection** - AI automatically decides when to use tools  
✅ **Addition Tool** - Can solve math problems like "What is 15 + 25?"  
✅ **Natural Conversation** - Regular chat without needing tools  
✅ **API Servers** - REST endpoints for integration  
✅ **Same Behavior** - Both versions work identically

## 🧠 **Why This Project?**

### **For Python Beginners:**

- 🐍 Clean, simple Python code with type hints
- 📚 Extensive comments and documentation
- 🚀 FastAPI with auto-generated docs
- 🔧 Follows official LangGraph patterns

### **For JavaScript Developers:**

- 🟨 Familiar syntax and patterns
- ⚡ Express.js server setup
- 🌐 Easy frontend integration
- 📦 Modern ES modules

### **For Learning:**

- 📊 **Compare both implementations** side-by-side
- 🔄 **Same logic, different syntax** - perfect for learning
- 📖 **Official LangGraph patterns** from documentation
- 🎨 **Visual comparisons** and flowcharts

## 🔄 **How It Works (Both Languages)**

The **LLM automatically decides** - no manual parsing needed!

```
User Input → LLM Analyzes → Needs Tools?
                              ↓
                         Math Question → Use Addition Tool
                         Regular Chat → Direct Response
```

## 🌐 **API Endpoints (Both Servers)**

| Endpoint  | Method | Description                     |
| --------- | ------ | ------------------------------- |
| `/`       | GET    | Welcome message                 |
| `/health` | GET    | System status                   |
| `/chat`   | POST   | Chat with agent                 |
| `/docs`   | GET    | API documentation (Python only) |

**Test the API:**

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Can you add 100 and 200?"}'
```

## 📚 **Learning Resources**

| File                                 | Purpose                          |
| ------------------------------------ | -------------------------------- |
| `src/README.md`                      | Python implementation guide      |
| `js/README.md`                       | JavaScript implementation guide  |
| `Python_vs_JavaScript_Comparison.md` | Detailed side-by-side comparison |
| `tutorial.md`                        | Step-by-step learning tutorial   |

## 🎨 **Why Google Gemini 1.5 Flash?**

✅ **Fast**: Quicker responses than other models  
✅ **Free**: No costs for basic usage  
✅ **Smart**: Excellent reasoning capabilities  
✅ **Reliable**: Google's stable API  
✅ **Tool-friendly**: Great at deciding when to use tools

## 🏃‍♂️ **Which Version Should You Use?**

**Choose Python 🐍 if:**

- You're learning LangChain/LangGraph
- You want better documentation
- You prefer simpler syntax
- You need type hints

**Choose JavaScript 🟨 if:**

- You're comfortable with JS
- You want frontend integration
- You prefer explicit configurations
- You're building web apps

**Try Both! 🚀** They work identically - great for learning!

## 💡 **Common Issues**

| Issue              | Solution                   |
| ------------------ | -------------------------- |
| `python not found` | Use `python3` instead      |
| `pip not found`    | Use `pip3` instead         |
| API key error      | Check your `.env` file     |
| Import errors      | Install dependencies first |

## 🆘 **Need Help?**

1. **Check the specific README** in `src/` or `js/` folders
2. **Read the comparison** in `Python_vs_JavaScript_Comparison.md`
3. **Follow the tutorial** in `tutorial.md`
4. **Look at console output** - it shows what's happening
5. **Try the setup script** - `python3 setup.py`

---

**Happy learning with both Python and JavaScript! 🐍🟨🚀**
