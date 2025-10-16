

from resumeagents.resume_parser import resume_parser_agent
from resumeagents.jd_matcher import jd_matcher_agent
from resumeagents.interview_agent import interview_agent
from resumeagents.feedback_agent import feedback_agent
from utils.extract_text_from_file import extract_text_from_file

def run_pipeline_from_file(file, jd_text, role):
    try:
        resume_text = extract_text_from_file(file)
        print("📄 Extracted Resume Text:\n", resume_text)
    except Exception as e:
        print("⚠️ Error reading file:", e)
        return f"Error reading file: {e}", "", "", ""

    try:
        parsed = resume_parser_agent.run(resume_text)
        match_score = jd_matcher_agent.run({"resume": parsed, "jd_text": jd_text})
        interview = interview_agent.run({"resume": parsed, "role": role})
        feedback = feedback_agent.run({"resume": parsed, "jd_text": jd_text})
        return parsed.json(), match_score, interview, feedback
    except Exception as e:
        print("⚠️ Error in agent pipeline:", e)
        return f"Error during processing: {e}", "", "", ""


with gr.Blocks() as demo:
    gr.Markdown("# 🧠 Resume Parser + Interview Helper")

    with gr.Row():
        file_input = gr.File(label="Upload Resume (.pdf or .docx)")
        jd_input = gr.Textbox(label="Paste Job Description", lines=10)
        role_input = gr.Textbox(label="Role Title", value="Software Engineer")

    with gr.Row():
        parsed_output = gr.Textbox(label="Parsed Resume")
        match_output = gr.Textbox(label="Match Score & Explanation")

    interview_output = gr.Textbox(label="Mock Interview Questions")
    feedback_output = gr.Textbox(label="Resume Feedback")

    submit_btn = gr.Button("Run Agentic Pipeline")
    submit_btn.click(run_pipeline_from_file,
                     inputs=[file_input, jd_input, role_input],
                     outputs=[parsed_output, match_output, interview_output, feedback_output])




demo.launch()
