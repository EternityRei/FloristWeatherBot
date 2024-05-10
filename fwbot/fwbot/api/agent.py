from typing import List, Any, Optional

from langchain_openai import ChatOpenAI
from langchain import hub
from langchain.agents import create_openai_functions_agent, AgentExecutor
from ..core.tools.google_search import search
from ..core.tools.weather_tool import current_weather_by_city, current_weather_by_coordinates
from fwbot.util.prompt import PREFIX
from ..core.tools.datetime_tool import datetime
from ..core.tools.storage_tool import get_existing_flowers


class Agent:
    """
    Provides methods for asking questions and get analysis from the context using LLM agent
    """

    def __init__(self, additional_tools: Optional[List[Any]] = []):
        self.model = ChatOpenAI()
        self.tool = [search, current_weather_by_city, current_weather_by_coordinates, datetime, get_existing_flowers] + additional_tools
        self.prompt = hub.pull("hwchase17/openai-functions-agent")
        self.prompt.messages[0].prompt.template = PREFIX
        self.agent = create_openai_functions_agent(self.model, self.tool, self.prompt)
        self.agent_executor = AgentExecutor(
            agent=self.agent,
            tools=self.tool,
            verbose=True,
            handle_parsing_errors=True
        )

    def ask(self, prompt: str, chat_history: Optional[List[Any]] = []):
        return self.agent_executor.invoke({'input': prompt, 'chat_history': chat_history})
