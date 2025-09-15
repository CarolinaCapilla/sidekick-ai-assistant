from langchain_community.agent_toolkits import FileManagementToolkit


def get_file_tools():
    toolkit = FileManagementToolkit(root_dir="sandbox")
    return toolkit.get_tools()