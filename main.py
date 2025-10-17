
import gradio as gr
import asyncio
import os
from dotenv import load_dotenv
from agents import Runner

# Load environment variables
load_dotenv(override=True)

# Verify API key is loaded
api_key = os.environ.get('OPENAI_API_KEY')
if not api_key:
    print("⚠️ WARNING: OPENAI_API_KEY not found in environment variables!")
else:
    print("✅ OPENAI_API_KEY loaded successfully")

from resumeagents.resume_parser import resume_parser_agent
from resumeagents.jd_matcher import jd_matcher_agent
from resumeagents.interview_agent import interview_agent
from resumeagents.feedback_agent import feedback_agent
from utils.extract_text_from_file import extract_text_from_file
import json

def format_resume_text(resume_data):
    """Convert resume JSON to readable text format"""
    try:
        if isinstance(resume_data, str):
            resume_dict = json.loads(resume_data)
        else:
            resume_dict = resume_data
            
        formatted_text = f"""Name: {resume_dict.get('name', 'N/A')}
Email: {resume_dict.get('email', 'N/A')}

Skills:
{chr(10).join([f"• {skill}" for skill in resume_dict.get('skills', [])])}

Experience:
{chr(10).join([f"• {exp}" for exp in resume_dict.get('experience', [])])}

Education:
{chr(10).join([f"• {edu}" for edu in resume_dict.get('education', [])])}"""
        
        return formatted_text
    except Exception as e:
        return f"Error formatting resume: {str(e)}"

def run_pipeline_sync(file, jd_text, role):
    """Synchronous wrapper for the async pipeline function"""
    return asyncio.run(run_pipeline_from_file(file, jd_text, role))

async def run_pipeline_from_file(file, jd_text, role):
    try:
        resume_text = extract_text_from_file(file)
        print("📄 Extracted Resume Text:\n", resume_text)
    except Exception as e:
        print("⚠️ Error reading file:", e)
        return f"Error reading file: {e}", "", "", ""

    try:
        parsed = await Runner.run(resume_parser_agent, resume_text)
        parsed_resume = parsed.final_output
        
        # Convert parsed resume to JSON string for other agents
        resume_json = parsed_resume.model_dump_json()
        
        # Create input strings for each agent
        match_input = f"Resume: {resume_json}\n\nJob Description: {jd_text}"
        interview_input = f"Resume: {resume_json}\n\nRole: {role}"
        feedback_input = f"Resume: {resume_json}\n\nJob Description: {jd_text}"
        
        match_score = await Runner.run(jd_matcher_agent, match_input)
        interview = await Runner.run(interview_agent, interview_input)
        feedback = await Runner.run(feedback_agent, feedback_input)
        
        # Format the resume for display
        formatted_resume = format_resume_text(resume_json)
        
        return formatted_resume, match_score.final_output, interview.final_output, feedback.final_output
    except Exception as e:
        print("⚠️ Error in agent pipeline:", e)
        return f"Error during processing: {e}", "", "", ""


with gr.Blocks(title="Resume Parser + Interview Helper", theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🧠 Resume Parser + Interview Helper")
    gr.Markdown("Upload your resume, paste a job description, and get AI-powered analysis!")

    with gr.Row():
        with gr.Column(scale=1):
            file_input = gr.File(label="📄 Upload Resume (.pdf or .docx)", file_types=[".pdf", ".docx"])
            jd_input = gr.Textbox(
                label="📝 Paste Job Description", 
                lines=10, 
                placeholder="Paste the job description here...",
                show_copy_button=True
            )
            role_input = gr.Textbox(
                label="💼 Role Title", 
                value="Software Engineer",
                placeholder="e.g., Software Engineer, Data Scientist..."
            )
            submit_btn = gr.Button("🚀 Run Agentic Pipeline", variant="primary", size="lg")

        with gr.Column(scale=2):
            parsed_output = gr.Textbox(
                label="📋 Parsed Resume", 
                lines=15, 
                max_lines=20,
                show_copy_button=True
                
            )
            match_output = gr.Textbox(
                label="🎯 Match Score & Analysis", 
                lines=8, 
                max_lines=15,
                show_copy_button=True
                
            )
            interview_output = gr.Textbox(
                label="❓ Mock Interview Questions", 
                lines=8, 
                max_lines=15,
                show_copy_button=True
               
            )
            feedback_output = gr.Textbox(
                label="💡 Resume Feedback", 
                lines=8, 
                max_lines=15,
                show_copy_button=True
                
            )

    submit_btn.click(
        run_pipeline_sync,
        inputs=[file_input, jd_input, role_input],
        outputs=[parsed_output, match_output, interview_output, feedback_output]
    )




demo.launch()
