from langchain_openai import ChatOpenAI
from langchain import hub
from langchain.agents import create_openai_functions_agent, AgentExecutor
from ..core.tools.google_search import search


class Agent:
    """
    Provides methods for asking questions and get analysis from the context using LLM agent
    """

    def __init__(self):
        self.model = ChatOpenAI()
        self.tool = [search]
        self.prompt = hub.pull("hwchase17/openai-functions-agent")
        self.agent = create_openai_functions_agent(self.model, self.tool, self.prompt)
        self.agent_executor = AgentExecutor(
            agent=self.agent,
            tools=self.tool,
            verbose=True,
            handle_parsing_errors=True
        )

    def ask(self, prompt: str):
        return self.agent_executor.invoke({'input': prompt})
