import os
from dotenv import load_dotenv
load_dotenv()
from crewai import Agent, Task, Crew, Process
from langchain.agents import AgentType, initialize_agent
from langchain_google_genai import ChatGoogleGenerativeAI 

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

llm = ChatGoogleGenerativeAI(model="gemini-pro",
                             verbose=True,
                             temperature=0.3,
                             google_api_key=GOOGLE_API_KEY)


print("## Welcome to the Game Builder")
print('-------------------------------')
game = input("What is the game you would like to build? What will be the mechanics?\n")


# Create Agents
senior_engineer_agent = Agent(
    role='Senior Software Engineer',
    goal='Create software as needed',
    backstory="""
				You are a Senior Software Engineer at a leading tech think tank.
				Your expertise in programming in python. and do your best to
				produce perfect code""",
    allow_delegation=False,
    verbose=True,
    llm=llm
    )

qa_engineer_agent = Agent(
    role='Software Quality Control Engineer',
    goal='create prefect code, by analizing the code that is given for errors',
    backstory="""
				You are a software engineer that specializes in checking code
  			for errors. You have an eye for detail and a knack for finding
				hidden bugs.
  			You check for missing imports, variable declarations, mismatched
				brackets and syntax errors.
  			You also check for security vulnerabilities, and logic errors""",
    allow_delegation=False,
    verbose=True,
    llm=llm
    )

chief_qa_engineer_agent = Agent(
    role='Chief Software Quality Control Engineer',
    goal='Ensure that the code does the job that it is supposed to do',
    backstory="""\
				You feel that programmers always do only half the job, so you are
				super dedicate to make high quality code.""",
    allow_delegation=True,
    verbose=True,
    llm=llm
    )


# Create Tasks
code_task = Task(
    description=f"""You will create a game using python, these are the instructions:

        Instructions
        ------------
    	{game}

        Your Final answer must be the full python code, only the python code and nothing else.
        """,
    agent=senior_engineer_agent
    )


review_task = Task(
    description=f"""
        You are helping create a game using python, these are the instructions:

        Instructions
        ------------
        {game}

        Using the code you got, check for errors. Check for logic errors,
        syntax errors, missing imports, variable declarations, mismatched brackets,
        and security vulnerabilities.

        Your Final answer must be the full python code, only the python code and nothing else.
        """,
    agent=qa_engineer_agent
    )

evaluate_task = Task(description=f"""
        You are helping create a game using python, these are the instructions:

        Instructions
        ------------
        {game}

        You will look over the code to insure that it is complete and
        does the job that it is supposed to do.

        Your Final answer must be the full python code, only the python code and nothing else.
        """,
			agent=chief_qa_engineer_agent
		)




crew = Crew(
  agents=[senior_engineer_agent,qa_engineer_agent,chief_qa_engineer_agent],
  tasks=[code_task,review_task,evaluate_task],
  verbose=True,
  process=Process.sequential
)


game = crew.kickoff()


# Print results
print("\n\n########################")
print("## Here is the result")
print("########################\n")
print("final code for the game:")
print(game)


# save it in python file
text_file = open("sample.py", "w")
n = text_file.write(game)
if n == len(game):
    print("Success! String written to text file.")
else:
    print("Failure! String not written to text file.")
text_file.close()