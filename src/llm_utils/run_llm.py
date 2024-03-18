import json
from typing import List, Dict, Tuple, Callable
from langchain_core.language_models.chat_models import BaseChatModel
from langchain.schema import (
    FunctionMessage,
    HumanMessage,
    AIMessage,
    BaseMessage,
    SystemMessage,
)

from typing import List, Dict, Tuple, Callable, Union


# Function to run the AI
def run_llm(
    system_message: SystemMessage,
    previous_messages: List[Union[HumanMessage, AIMessage]],
    chat_llm: BaseChatModel,
    toolbox: Dict[str, Tuple[dict, Callable]],
    max_function_iterations: int = 3,
) -> AIMessage:
    """
    Run the AI

    Args:
        system_message (SystemMessage): System message of the Agent
        human_message (HumanMessage): Human message to the Agent
        chat_llm (BaseChatModel): Chat model to use
        toolbox (Dict[str, Tuple[dict, Callable]]): Toolbox (can be an empty dictionary)
        max_function_iterations (int, optional): Maximum number of iterations. Defaults to 3.

    Returns:
        AIMessage: Response from the AI
    """
    print("Running AI")
    # Create the history SystemMessage + HumanMessage )
    History = [system_message] + previous_messages

    if len(toolbox) == 0:  # if toolbox is empty, we don't need to pass the functions
        response = chat_llm.invoke(History)  # Chain mode
    else:
        function_name_list = [tool[0] for tool in toolbox.values()]  # Agent mode
        response = chat_llm.invoke(
            History, functions=function_name_list
        )  # Agent is invoked with the functions

    function_iteration = 0
    # If the response has a function call (only in agent mode) we need to call the function
    while "function_call" in response.additional_kwargs.keys():
        print("Function call detected")
        function_name = response.additional_kwargs["function_call"]["name"]
        function_arguments = response.additional_kwargs["function_call"]["arguments"]

        print(
            f"Llamando a la función: {function_name} \nArgumentos: {function_arguments}"
        )

        # Arguments
        try:
            str_arguments = json.loads(function_arguments)
        except:
            str_arguments = function_arguments

        # Function is called
        try:
            function_result = str(toolbox[function_name][1](**str_arguments))

        except KeyError as e:
            print(f"Error: {e}")
            function_result = f"La función {function_name} no existe. Las funciones disponibles son: {list(toolbox.keys())}."

        print(f"Resultado: {function_result}")

        # Function message is created
        function_msg = FunctionMessage(name=function_name, content=str(function_result))

        # Function message is added to the history
        History.append(function_msg)

        # If the number of iterations is less than the maximum, the LLM is called again
        if function_iteration < max_function_iterations:
            response = chat_llm.invoke(
                History,
                functions=function_name_list,
            )

        else:  # If the number of iterations is greater than the maximum, the LLM is called without functions
            response = chat_llm.invoke(
                History,
                functions=function_name_list,
                function_call="none",
            )

        History.append(response)  # The response is added to the history

        function_iteration += 1  # The number of iterations is increased

    return response  # The response is returned
