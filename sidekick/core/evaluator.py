from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from typing import List, Any, Dict
import logging
from sidekick.core.state import EvaluatorOutput, State
from config.settings import DEFAULT_MODEL

# Set up logging
logger = logging.getLogger(__name__)

class Evaluator:
    """
    Evaluator class that assesses whether a task has been completed successfully.
    
    This class is responsible for evaluating the assistant's responses against
    the success criteria and determining if more user input is needed.
    """
    
    def __init__(self):
        """Initialize the Evaluator with the appropriate LLM."""
        evaluator_llm = ChatOpenAI(model=DEFAULT_MODEL)
        self.evaluator_llm_with_output = evaluator_llm.with_structured_output(EvaluatorOutput)
    
    def format_conversation(self, messages: List[Any]) -> str:
        """
        Format a conversation history into a readable string.
        
        Args:
            messages: List of message objects from the conversation history.
            
        Returns:
            str: Formatted conversation as a string.
        """
        conversation = "Conversation history:\n\n"
        for message in messages:
            if isinstance(message, HumanMessage):
                conversation += f"User: {message.content}\n"
            elif isinstance(message, AIMessage):
                text = message.content or "[Tools use]"
                conversation += f"Assistant: {text}\n"
        return conversation
    
    def evaluate(self, state: State) -> State:
        """
        Evaluate the assistant's response based on the success criteria.
        
        Args:
            state: The current state containing messages and success criteria.
            
        Returns:
            State: Updated state with evaluation results.
        """
        last_response = state["messages"][-1].content
        
        system_message = """You are an evaluator that determines if a task has been completed successfully by an Assistant.
    Assess the Assistant's last response based on the given criteria. Respond with your feedback, and with your decision on whether the success criteria has been met,
    and whether more input is needed from the user."""
        
        user_message = f"""You are evaluating a conversation between the User and Assistant. You decide what action to take based on the last response from the Assistant.

    The entire conversation with the assistant, with the user's original request and all replies, is:
    {self.format_conversation(state["messages"])}

    The success criteria for this assignment is:
    {state["success_criteria"]}

    And the final response from the Assistant that you are evaluating is:
    {last_response}

    Respond with your feedback, and decide if the success criteria is met by this response.
    Also, decide if more user input is required, either because the assistant has a question, needs clarification, or seems to be stuck and unable to answer without help.

    The Assistant has access to a tool to write files. If the Assistant says they have written a file, then you can assume they have done so.
    Overall you should give the Assistant the benefit of the doubt if they say they've done something. But you should reject if you feel that more work should go into this.

    """
        if state["feedback_on_work"]:
            user_message += f"Also, note that in a prior attempt from the Assistant, you provided this feedback: {state['feedback_on_work']}\n"
            user_message += "If you're seeing the Assistant repeating the same mistakes, then consider responding that user input is required."
        
        evaluator_messages = [
            SystemMessage(content=system_message),
            HumanMessage(content=user_message),
        ]
        
        eval_result = self.evaluator_llm_with_output.invoke(evaluator_messages)
        new_state = {
            "messages": [
                {
                    "role": "assistant",
                    "content": f"Evaluator Feedback on this answer: {eval_result.feedback}",
                }
            ],
            "feedback_on_work": eval_result.feedback,
            "success_criteria_met": eval_result.success_criteria_met,
            "user_input_needed": eval_result.user_input_needed,
        }
        return new_state
    
    def route_based_on_evaluation(self, state: State) -> str:
        """
        Determine the next step based on the evaluation results.
        
        Args:
            state: The current state after evaluation.
            
        Returns:
            str: The next node to route to ("worker" or "END").
        """
        if state["success_criteria_met"]:
            logger.info("Success criteria met, ending graph execution")
            return "END"
        elif state["user_input_needed"]:
            logger.info("User input needed, ending graph execution")
            return "END"
        else:
            logger.info("Success criteria not met, continuing with worker")
            return "worker"
