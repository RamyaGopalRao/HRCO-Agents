from agents import Agent
from models.resume_schema import Resume

INSTRUCTIONS = """
You are a resume parsing expert. Given raw resume text, extract structured data in JSON format.
Return keys: name, email, skills (list), experience (list), education (list).
"""

resume_parser_agent = Agent(
    name="ResumeParserAgent",
    instructions=INSTRUCTIONS,
    model="gpt-4o-mini",
    output_type=Resume
)
