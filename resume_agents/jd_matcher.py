from agents import Agent
from models.resume_schema import Resume
from pydantic import BaseModel

INSTRUCTIONS = """
You are a resume matching expert. Given a structured resume and a job description, compare them and score the match from 0 to 100.
Return a short explanation of the score and highlight key strengths or gaps.
"""

class JDMatchRequest(BaseModel):
    resume: Resume
    jd_text: str

jd_matcher_agent = Agent(
    name="JDMatcherAgent",
    instructions=INSTRUCTIONS,
    model="gpt-4o-mini",
    output_type=str
)
