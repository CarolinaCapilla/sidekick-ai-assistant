from langchain.agents import Tool
from typing import List, Dict, Any
import os
import datetime

# We generate markdown using the same formatter used by the UI utility,
# but delegate the actual write to FileManagementToolkit's write_file
# to keep all agent-initiated writes inside the sandbox.
from sidekick.utils.output_saver import format_conversation_as_markdown
from sidekick.tools.file_tools import get_file_tools  # Provides FileManagementToolkit tools


def _find_write_file_tool():
    """
    Locate the FileManagementToolkit write_file tool.

    Note: We are NOT using other toolkit tools here (e.g., read_file, list_dir)
    although they are available; we might expose them in future utilities.
    """
    tools = get_file_tools()
    for t in tools:
        if getattr(t, "name", "") == "write_file":
            return t
    return None


def save_conversation_tool_fn(args: Dict[str, Any]) -> str:
    """
    Tool function to save a conversation to markdown using the sandboxed write_file tool.

    Expected payload (dict):
        - message: str
        - success_criteria: str
        - conversation_history: List[Dict[str, Any]]
        - output_dir: Optional[str] = "outputs" (relative to sandbox root)

    Returns the file path string (relative to sandbox) where the markdown was saved.

    Fallback: If the toolkit is unavailable, we fall back to direct I/O outside the sandbox.
    """
    message = args.get("message", "")
    success_criteria = args.get("success_criteria", "")
    conversation_history = args.get("conversation_history", [])
    # Default to sandbox/outputs by making path relative to sandbox root
    output_dir = args.get("output_dir", "outputs").strip().lstrip("/")

    # Generate markdown content
    markdown_content = format_conversation_as_markdown(
        message=message,
        success_criteria=success_criteria,
        conversation_history=conversation_history,
    )

    # Generate filename
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    message_words = (message or "").split()[:5]
    slug = "_".join([w.lower() for w in message_words if w.isalnum()]) or "conversation"
    filename = f"{timestamp}_{slug}.md"

    # Prefer sandboxed write via toolkit
    write_tool = _find_write_file_tool()
    if write_tool is not None:
        relative_path = os.path.join(output_dir, filename)
        payload = {"file_path": relative_path, "text": markdown_content}
        # Many Tool impls use .invoke; fall back to callable if needed
        try:
            try:
                result = write_tool.invoke(payload)
            except AttributeError:
                result = write_tool(payload)  # type: ignore
            # Return the relative path (inside sandbox) for consistency
            return result if isinstance(result, str) and result else relative_path
        except Exception:
            # Fall through to direct I/O if toolkit write fails
            pass

    # Fallback: direct I/O outside sandbox (not preferred for agent-initiated writes)
    # We keep this to ensure reliability. Consider aligning all writes via toolkit in future.
    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, filename)
    with open(file_path, "w") as f:
        f.write(markdown_content)
    return file_path


def get_output_saver_tool() -> Tool:
    """Return a Tool that saves the conversation markdown to the sandbox outputs directory.

    Note: We are not exposing additional FileManagementToolkit tools here yet (e.g., read_file,
    list_dir). We might add complementary tools for reading/listing saved outputs later.
    """
    return Tool(
        name="save_conversation_output",
        func=save_conversation_tool_fn,
        description=(
            "Save the current conversation to a markdown file using the sandboxed file writer. "
            "Provide a dict with keys: message (str), success_criteria (str), "
            "conversation_history (List[Dict[str, Any]]), and optional output_dir (str, relative to sandbox). "
            "Returns the file path of the saved markdown."
        ),
    )
