from crewai import Agent, Task, Crew, LLM, Process
from crewai_tools import SerperDevTool
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

_ = load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
gemini_llm = LLM(
    model = "gemini/gemini-2.0-flash",
    api_key = GEMINI_API_KEY
)

def generate_flashcards(topic):
    """Creates flashcards using CrewAI for the given topic."""
    
    # Define the Flashcard Agent
    flashcard_agent = Agent(
        role="Flashcard Creator",
        goal=f"Generate flashcards on {topic}.",
        backstory="You are an expert tutor who creates concise, easy-to-understand flashcards.",
        llm=gemini_llm,
        verbose=True
    )

    # Define Task
    flashcard_task = Task(
        description=f"""
        Create 5 flashcards about '{topic}'. 
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
        agents=[flashcard_agent],
        tasks=[flashcard_task]
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
