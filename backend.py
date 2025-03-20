from crewai import Agent, Task, Crew, LLM, Process
from langchain_community.tools import TavilySearchResults
from dotenv import load_dotenv
import os
from crewai.tools import BaseTool
from pydantic import Field

_ = load_dotenv()
GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]
gemini_llm = LLM(
    model = "gemini/gemini-2.0-flash",
    api_key = GEMINI_API_KEY
)

TAVILY_API_KEY = os.environ["TAVILY_API_KEY"]

tavily = TavilySearchResults(
    max_results=5,
    search_depth="advanced",
    include_answer=True,
    include_raw_content=True,
    include_images=True
)

class SearchTool(BaseTool):
    name: str = "Search"
    description: str = "Useful for search-based queries. Use this to find information about given topic."
    search: TavilySearchResults = Field(default_factory=TavilySearchResults)

    def _run(self, query: str) -> str:
        try:
            return self.search.run(query)
        except Exception as e:
            return f"Error performing search: {str(e)}"

def generate_flashcards(topic):
    """Creates flashcards using CrewAI for the given topic."""
    planner_agent = Agent(
        role="Flashcard Topics Planner",
        goal=f"Plan the topics for {topic} that can be useful for studying.",
        backstory="You are an expert tutor who creates a study plan with 5 topics that can be converted into flashcards",
        llm=gemini_llm,
        verbose=True
    )

    planner_task = Task(
        description=f"""
        Create a study plan for '{topic}'. 
        Include all important topics for it and return the list, with no more than 3 topics. 
        This will be used by the search agent to search the web and create flashcards on these topics.
        """,
        expected_output="3 topics, with 1-2 high quality SEO keywords each that can be used to find good factually correct content for the flashcards",
        agent=planner_agent
    )

    search_agent = Agent(
        role="Search Agent",
        goal=f"Search the web for content that will be used to create flashcards on the topic: {topic} using the output from the planner agent",
        backstory="You are an expert researcher that can extract SEO keywords (combine if needed) from the output of the planner agent and search the internet",
        llm=gemini_llm,
        tools=[SearchTool()]
    )

    search_task = Task(
        description=f"""
        Search the internet using the SearchTool using the SEO keywords from the output from the planner agent. 
        Search through only 1 internet resource per SEO keyword.
        Return 3 bullet points per topic that can be converted into flashcards. 
        """,
        expected_output="3 bullet points for each of the 3 topics returned by planner agent with factually correct information.",
        agent=search_agent
    )



    # Define the Flashcard Agent
    flashcard_agent = Agent(
        role="Flashcard Creator",
        goal=f"Generate flashcards on {topic} using the output from the search agent.",
        backstory="You are an expert tutor who creates concise, easy-to-understand flashcards.",
        llm=gemini_llm,
        verbose=True
    )

    # Define Task
    flashcard_task = Task(
        description=f"""
        Create 5 flashcards about '{topic}' using the output from the search agent.
        Choose 5 questions from the 25 possible questions you have from the search agent's output. 
        Choose one bullet point per topic and convert it into a flashcard.
        Each flashcard should have a question and an answer.
        
        Format each flashcard as:
        Q: [Question here]
        A: [Answer here]
        
        Make sure the answers are concise and accurate.
        """,
        expected_output="5 flashcards, each with a question and an answer",
        agent=flashcard_agent
    )

    # Create Crew and Assign Task
    crew = Crew(
        agents=[planner_agent, search_agent, flashcard_agent],
        tasks=[planner_task, search_task, flashcard_task]
    )

    # Run CrewAI
    result = crew.kickoff()

    if not isinstance(result.raw, str):
        return []
    
    # Split the raw output into segments based on double newlines
    flashcards = []
    raw_cards = result.raw.split("\n\n")
    
    # For each segment, assume the first line is the question and the second is the answer
    for segment in raw_cards:
        lines = segment.strip().split("\n")
        if len(lines) >= 2:
            question = lines[0].replace("Q:", "").strip()
            answer = lines[1].replace("A:", "").strip()
            flashcards.append({"question": question, "answer": answer})
    
    return flashcards

if __name__ == "__main__":
    result = generate_flashcards("Mitochondria")
    print("\nGenerated Flashcards:")
    print(result)
