# AI-Powered ATS Resume Analyzer

![ATS Analyzer](https://img.shields.io/badge/AI-Powered-blue) ![Python](https://img.shields.io/badge/Python-3.8%2B-green) ![FastAPI](https://img.shields.io/badge/FastAPI-0.95%2B-teal) 

An intelligent Application Tracking System (ATS) Resume Analyzer that leverages the power of Large Language Models (LLMs) to evaluate resumes against job descriptions. It provides detailed feedback, match scores, and actionable recommendations to help candidates improve their improved chances.

## 🚀 Live Demo

Try out the deployed application on Hugging Face Spaces:
**[👉 Live ATS Resume Analyzer](https://huggingface.co/spaces/Rahma07/ATS)**

## ✨ Key Features

- **📄 PDF Resume Parsing**: robust extraction of text from PDF resumes.
- **🤖 AI-Powered Analysis**: Uses Groq API and LangChain to perform deep semantic analysis.
- **📊 Structured Feedback**:
    - **Match Percentage**: Quantitative score indicating fit.
    - **Missing Keywords**: Identifies critical skills and terms missing from the resume.
    - **Profile Summary**: Generates a professional summary tailored to the job.
- **💡 Actionable Recommendations**: Specific advice on how to improve the resume for the target role.
- **⚡ Fast & Modern UI**: Built with FastAPI and pure HTML/CSS for a responsive experience.

## 🛠️ Technology Stack

- **Backend**: Python, FastAPI
- **LLM Integration**: LangChain, LangChain Groq
- **Frontend**: Jinja2 Templates, HTML5, CSS3
- **PDF Processing**: pypdf

## 📋 Prerequisites

Ensure you have the following installed:
- Python 3.8 or higher
- git

## ⚙️ Installation

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/Rahma07/ATS.git
    cd ATS
    ```

2.  **Create and Activate a Virtual Environment**
    ```bash
    # Windows
    python -m venv venv
    venv\Scripts\activate

    # macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

## 🔐 Configuration

1.  **Environment Variables**
    Copy the example environment file to create your local configuration:
    ```bash
    cp app/.env.example app/.env
    # Or on Windows CMD
    copy app\.env.example app\.env
    ```

2.  **Set Up API Keys**
    Open `app/.env` and add your Groq API key:
    ```env
    GROQ_API_KEY=your_actual_api_key_here
    GROQ_MODEL_NAME="meta-llama/llama-3.3-70b-versatile"
    ```
    *Note: You can obtain a free API key from [Groq Console](https://console.groq.com/).*

## 🏃‍♂️ Usage

1.  **Start the Application**
    ```bash
    uvicorn app.main:app --reload
    ```

2.  **Access the Interface**
    Open your browser and navigate to:
    `http://127.0.0.1:8000`

3.  **Analyze a Resume**
    - Paste the **Job Description** into the text area.
    - Upload your **Resume (PDF)**.
    - Click **Analyze Resume**.
    - Review the AI-generated feedback and match score.

## 📂 Project Structure

```
ATS/
├── app/
│   ├── api/            # API routes and schemas
│   ├── core/           # Configuration and prompts
│   ├── services/       # Business logic (LLM, Analysis)
│   ├── static/         # CSS, Images
│   ├── templates/      # HTML Templates
│   ├── utils/          # Utility functions (File processing)
│   ├── main.py         # Application entry point
│   └── dependencies.py # Dependency injection
├── requirements.txt    # Python dependencies
└── README.md           # Project documentation
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License.
