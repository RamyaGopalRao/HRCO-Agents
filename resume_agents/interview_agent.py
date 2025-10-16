from agents import Agent
from models.resume_schema import Resume
from pydantic import BaseModel

INSTRUCTIONS = """
You are an expert interviewer for technical roles. Given a candidate's resume and the target role, generate 3 behavioral and 2 technical interview questions tailored to their background.
Return the questions as a single formatted string.
"""

class InterviewRequest(BaseModel):
    resume: Resume
    role: str

interview_agent = Agent(
    name="InterviewAgent",
    instructions=INSTRUCTIONS,
    model="gpt-4o-mini",
    output_type=str
)
