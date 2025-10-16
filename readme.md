

---

## 🏗️ Architecture

This project follows a modular agentic architecture using OpenAI's GPT-4o and custom orchestration. Each agent is responsible for a distinct task:

- **ResumeParserAgent**: Parses uploaded resumes (PDF/DOCX) into structured JSON using Pydantic.
- **JDMatcherAgent**: Compares resume data with a job description and returns a match score.
- **InterviewAgent**: Generates tailored interview questions based on candidate profile and job role.
- **FeedbackAgent**: Suggests resume improvements and missing skills.

Agents are orchestrated using a custom `Runner` and `trace` abstraction, enabling sequential execution and traceable outputs. The UI is built with Gradio for interactive resume upload and result display.

---

## 🚀 How to Run

### 1. **Install dependencies**
```bash
pip install -r requirements.txt
```

### 2. **Set your OpenAI API key**
Create a `.env` file in the root directory:
```
OPENAI_API_KEY=your-key-here
```

### 3. **Start the Gradio app**
```bash
python main.py
```

### 4. **Upload a resume and paste a job description**
The app will:
- Parse the resume
- Match it to the job description
- Simulate interview questions
- Provide feedback


