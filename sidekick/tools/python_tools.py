from langchain_experimental.tools import PythonREPLTool

def get_python_repl_tool():
    """Get a tool for executing Python code in a REPL environment"""
    return PythonREPLTool()
