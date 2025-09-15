# Sidekick Personal Co-Worker

An intelligent AI assistant that helps you complete tasks through a conversational interface. Built with LangGraph and currently using Gradio for the web interface, with plans to migrate to a more robust Flask + Vue.js architecture.

## 🚀 Features

- **AI-Powered Task Completion**: Uses specialized agents to understand and execute your requests
- **Multi-Agent Architecture**: Worker and evaluator agents working together to meet success criteria
- **Web Interface**: Clean Gradio UI for easy interaction
- **Web Browsing Capabilities**: Built-in browser automation with Playwright
- **Push Notifications**: Optional push notifications via Pushover
- **Modular Design**: Easy to extend with additional tools

## 🏗️ Architecture

The system consists of several specialized components:

- **Worker Agent**: Performs tasks and uses tools to complete user requests
- **Evaluator Agent**: Assesses if the success criteria have been met
- **Tool System**: Includes web browsing, file management, search, and more
- **LangGraph Workflow**: Orchestrates the entire task completion pipeline

## 📋 Prerequisites

- Python 3.8+
- OpenAI API key
- Pushover credentials (optional)
- Google Serper API key (for web search)

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/username/sidekick.git
   cd sidekick
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   Create a `.env` file in the root directory:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   PUSHOVER_TOKEN=your_pushover_token_here
   PUSHOVER_USER=your_pushover_user_here
   SERPER_API_KEY=your_serper_api_key_here
   ```

## 🚀 Usage

### Running the Web App

```bash
python app.py
```

This will launch a Gradio web interface where you can:
1. Enter your request to the Sidekick
2. Specify your success criteria
3. Click "Go!" to start the process
4. View real-time conversation updates
5. Reset the conversation when needed

### Example Interactions

- "Find the latest news about artificial intelligence and summarize the top 3 stories"
- "Create a Python script that analyzes stock market data"
- "Research the health benefits of meditation and create a report"

## 📁 Project Structure

```
sidekick_app/
├── app.py              # Main Gradio web application
├── sidekick.py         # Core Sidekick implementation with LangGraph
├── sidekick_tools.py   # Tools implementation (browser, search, etc.)
├── sandbox/            # Directory for file operations
└── README.md           # This file
```

## 🔧 Configuration

### Agent Configuration

The Sidekick uses GPT-4o-mini by default, but you can modify the model in `sidekick.py`:

```python
worker_llm = ChatOpenAI(model="gpt-4o-mini")  # Change to your preferred model
```

### Tool Configuration

Additional tools can be added in `sidekick_tools.py`:

```python
async def other_tools():
    # Add your custom tools here
    custom_tool = Tool(name="tool_name", func=tool_function, description="Tool description")
    return existing_tools + [custom_tool]
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🐛 Troubleshooting

### Common Issues

1. **Browser not launching**: Make sure Playwright is installed correctly
2. **API errors**: Verify your API keys are correct in the `.env` file
3. **Gradio not starting**: Ensure port 7860 is available
4. **Push notifications not working**: Check your Pushover configuration

### Debug Mode

To see more detailed logs:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 🔄 Future Enhancements

### Flask + Vue UI Migration

- [ ] **Backend API Development**
  - [ ] Create Flask API endpoints for Sidekick functionality
  - [ ] Implement WebSocket support for real-time updates
  - [ ] Design RESTful API for conversation management
  - [ ] Add authentication middleware and user sessions

- [ ] **Vue.js Frontend**
  - [ ] Set up Vue 3 project with Composition API
  - [ ] Create responsive chat interface components
  - [ ] Implement Vuex store for state management
  - [ ] Design modern UI with Tailwind CSS or Vuetify

- [ ] **DevOps & Deployment**
  - [ ] Configure Docker containers for Flask and Vue
  - [ ] Set up CI/CD pipeline for automated testing and deployment
  - [ ] Implement environment-specific configurations

### Other Enhancements

- [ ] Add support for additional LLM providers
- [ ] Implement conversation history persistence
- [ ] Add user authentication and multi-user support
- [ ] Implement task scheduling
- [ ] Add voice input/output capabilities

## 📞 Support

If you encounter any issues or have questions:

1. Check the Issues page
2. Create a new issue with detailed information
3. Include error messages and steps to reproduce

---

**Made with ❤️ using LangGraph and Gradio** (Future: Flask + Vue.js)
