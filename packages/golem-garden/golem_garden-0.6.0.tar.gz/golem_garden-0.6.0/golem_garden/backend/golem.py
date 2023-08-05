import logging
import os

from dotenv import load_dotenv
from langchain.agents import Tool, initialize_agent, AgentType
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory



load_dotenv()

from langchain import SerpAPIWrapper, WikipediaAPIWrapper, WolframAlphaAPIWrapper

logger = logging.getLogger(__name__)

class Golem:
    def __init__(self):
        logger.info("Initializing Golem...")
        self._serper_search = SerpAPIWrapper(serpapi_api_key=os.environ["SERPER_API_KEY"])
        self._wikipedia_search = WikipediaAPIWrapper()
        self._wolfram_alpha = WolframAlphaAPIWrapper(wolfram_alpha_appid=os.environ["WOLFRAM_ALPHA_APPID"])
        self._tools = [
            Tool(
                name="Current Search",
                func=self._serper_search.run,
                description="useful for when you need to answer questions about current events or the current state of the world."
                            " the input to this should be a single search term."
            ),
            Tool(
                name="Wikipedia",
                func=self._wikipedia_search.run,
                description="useful when you what encyclopedic information about a topic."
            ),
            Tool(
                name="Wolfram Alpha",
                func=self._wolfram_alpha.run,
                description="useful when you need to answer questions about the world around you."
            )
        ]
        self._memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        self._index = None
        self._llm = ChatOpenAI(temperature=.8, model_name="gpt-4")
        self._chain = initialize_agent(self._tools,
                                       self._llm,
                                       agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
                                       verbose=True,
                                       memory=self._memory)

    def intake_message(self, message: str):
        logger.info(f"Received message: {message}")
        response = self._chain.run(message)
        return response
