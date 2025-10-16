from agents import Agent
from models.resume_schema import Resume
from pydantic import BaseModel

INSTRUCTIONS = """
You are a resume improvement expert. Given a candidate's structured resume and a job description, provide personalized suggestions to improve the resume for better alignment.
Focus on missing skills, formatting tips, and tailoring advice.
"""

class FeedbackRequest(BaseModel):
    resume: Resume
    jd_text: str

feedback_agent = Agent(
    name="FeedbackAgent",
    instructions=INSTRUCTIONS,
    model="gpt-4o-mini",
    output_type=str
)
