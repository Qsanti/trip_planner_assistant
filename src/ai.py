import os
from typing import List, Dict
from datetime import datetime

from langchain_openai import ChatOpenAI
from langchain.prompts.chat import (
    SystemMessagePromptTemplate,
)
from langchain.schema import HumanMessage, AIMessage

# Get LLM model
LLM_MODEL = os.environ.get("LLM_MODEL", "gpt-4-0125-preview")

# Create the chat model
chat_llm = ChatOpenAI(
    temperature=0.2,
    model_name=LLM_MODEL,
    request_timeout=60,
)

# Import the prompts
from .prompts.tripy_system import system_message_prompt as tripy_system_message_prompt

from .prompts.get_route_info_function_dict import (
    function_dictionary as consult_routes_function_dict,
)
from .prompts.add_route_funtion_dict import (
    function_dictionary as add_route_to_travel_plan_function_dict,
)
from .prompts.get_mixed_route_function_dict import (
    function_dictionary as get_mixed_routes_info_function_dict,
)

# Import the functions
from .functions.functions import (
    get_posible_routes_info,
    add_route_to_travel_plan,
    get_mixed_routes_info,
)

toolbox = {}
toolbox["consult_route_info"] = (consult_routes_function_dict, get_posible_routes_info)
toolbox["add_route_to_travel_plan"] = (
    add_route_to_travel_plan_function_dict,
    add_route_to_travel_plan,
)
toolbox["consult_mix_routes_info"] = (
    get_mixed_routes_info_function_dict,
    get_mixed_routes_info,
)


# Import the function to run the AI
from .llm_utils.run_llm import run_llm


def generate_response(messages: List[Dict[str, str]]) -> str:
    system_message_template = SystemMessagePromptTemplate.from_template(
        tripy_system_message_prompt
    )
    system_message_params = {"date": datetime.now().strftime("%Y-%m-%d-%H:%M:%S")}
    system_message = system_message_template.format(**system_message_params)

    previous_messages = [
        (
            HumanMessage(message["content"])
            if message["role"] == "user"
            else AIMessage(message["content"])
        )
        for message in messages
    ]
    try:
        # Run the LLM
        response = run_llm(
            system_message=system_message,
            previous_messages=previous_messages,
            chat_llm=chat_llm,
            toolbox=toolbox,
        )

    except Exception as e:
        print(e)
        response = AIMessage(
            content="There was an error running the AI. Please refresh the page and try again.",
        )

    return response.content
