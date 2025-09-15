import os
import datetime
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)

def save_conversation_to_markdown(
    message: str, 
    success_criteria: str, 
    conversation_history: List[Dict[str, Any]],
    output_dir: str = "outputs"
) -> str:
    """
    Save the conversation output to a markdown file.
    
    Args:
        message: The user's original message/request
        success_criteria: The success criteria for the task
        conversation_history: The conversation history including the final output
        output_dir: Directory where output files will be saved
        
    Returns:
        str: Path to the saved markdown file
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate a timestamp for the filename
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Create a filename based on the first few words of the message
    message_words = message.split()[:5]
    message_slug = "_".join([word.lower() for word in message_words if word.isalnum()])
    
    # Combine timestamp and message slug for the filename
    filename = f"{timestamp}_{message_slug}.md"
    file_path = os.path.join(output_dir, filename)
    
    # Format the conversation as markdown
    markdown_content = format_conversation_as_markdown(message, success_criteria, conversation_history)
    
    # Write to file
    try:
        with open(file_path, "w") as f:
            f.write(markdown_content)
        logger.info(f"Conversation saved to {file_path}")
        return file_path
    except Exception as e:
        logger.error(f"Error saving conversation to markdown: {e}")
        return ""

def format_conversation_as_markdown(
    message: str, 
    success_criteria: str, 
    conversation_history: List[Dict[str, Any]]
) -> str:
    """
    Format the conversation history as markdown.
    
    Args:
        message: The user's original message/request
        success_criteria: The success criteria for the task
        conversation_history: The conversation history
        
    Returns:
        str: Formatted markdown content
    """
    # Start with a title and metadata
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    markdown = f"# Sidekick Conversation Output\n\n"
    markdown += f"**Date:** {timestamp}\n\n"
    
    # Add the original request and success criteria
    markdown += "## Original Request\n\n"
    markdown += f"{message}\n\n"
    
    markdown += "## Success Criteria\n\n"
    markdown += f"{success_criteria}\n\n"
    
    # Add the conversation history
    markdown += "## Conversation\n\n"
    
    # Extract the final response (excluding the evaluator feedback)
    final_response = ""
    
    for i, entry in enumerate(conversation_history):
        role = entry.get("role", "")
        content = entry.get("content", "")
        
        if role == "user":
            markdown += f"### User\n\n{content}\n\n"
        elif role == "assistant":
            if i == len(conversation_history) - 2:  # The second-to-last entry is the final response
                final_response = content
            
            if "Evaluator Feedback" in content:
                markdown += f"### Evaluator Feedback\n\n{content.replace('Evaluator Feedback on this answer: ', '')}\n\n"
            else:
                markdown += f"### Assistant\n\n{content}\n\n"
    
    # Add a dedicated section for the final output
    markdown += "## Final Output\n\n"
    markdown += final_response
    
    return markdown
