# -*- coding: utf-8 -*-
"""
Service layer for handling the core analysis logic.
"""

import logging
import re
from typing import Optional

from langchain_core.exceptions import LangChainException
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
from pydantic import SecretStr

from app.api.schemas import AnalysisResult

# Initialize logger
logger = logging.getLogger(__name__)

class ATSAnalyzer:
    """
    Handles text extraction from files and AI-powered analysis using a structured output approach.
    """

    def __init__(
        self,
        groq_api_key: str,
        model_name: str,
        temperature: float = 0.0,
        max_input_length: int = 3000,
    ):
        """
        Initializes the analyzer with the Groq LLM and a JSON output parser.

        Args:
            groq_api_key: The API key for the Groq service.
            model_name: The name of the model to use for analysis.
            temperature: The temperature setting for the LLM.
            max_input_length: The maximum character length for input text.
        """
        if not groq_api_key:
            logger.error("GROQ_API_KEY is not configured.")
            raise ValueError("GROQ_API_KEY cannot be empty.")
        
        self.llm = ChatGroq(
            api_key=SecretStr(groq_api_key),
            model=model_name,
            temperature=temperature,
            model_kwargs={"response_format": {"type": "json_object"}},
        )
        self.parser = JsonOutputParser(pydantic_object=AnalysisResult)
        self.max_input_length = max_input_length
        logger.info(f"ATSAnalyzer initialized with model: {model_name}")

    def _clean_text(self, text: str) -> str:
        """
        A private helper method to clean and truncate text.
        
        Args:
            text: The input string to clean.
            
        Returns:
            The cleaned and truncated string.
        """
        # Remove multiple spaces and newlines
        text = re.sub(r'\s+', ' ', text)
        # Remove non-ASCII characters to prevent encoding issues
        text = re.sub(r'[^\x00-\x7F]+', '', text)
        # Truncate text to the maximum length
        return text.strip()[:self.max_input_length]

    def get_structured_analysis(
        self, resume_text: str, job_description: str
    ) -> Optional[AnalysisResult]:
        """
        Generates a structured analysis from the Llama model.

        Args:
            resume_text: The extracted text from the resume.
            job_description: The job description text.

        Returns:
            An AnalysisResult object, or None on failure.
        """
        logger.info("Cleaning and validating input texts.")
        resume_text_clean = self._clean_text(resume_text)
        job_description_clean = self._clean_text(job_description)

        if len(resume_text_clean) < 100:
            logger.error(
                "Extracted resume text is too short (%d chars). The file may be empty or image-based.",
                len(resume_text_clean)
            )
            return None
        if len(job_description_clean) < 50:
            logger.error(
                "Job description text is too short (%d chars). Please provide a detailed job description.",
                len(job_description_clean)
            )
            return None

        # This prompt template is crucial for guiding the LLM to produce the desired JSON output.
        # It sets the persona, objective, and provides detailed instructions for the analysis.
        prompt_template = """**Role:** You are an expert AI-powered Applicant Tracking System (ATS) with the persona of a seasoned, insightful, and constructive senior hiring manager. Your goal is to provide a fair, balanced, and helpful analysis.

**Objective:** Analyze the provided resume against the job description and return a structured JSON object with your findings. The analysis must be objective, factual, and strictly based on the text provided.

**Analysis Steps & Tone:**

1.  **Critical Requirements Extraction:** Identify all non-negotiable requirements from the job description (e.g., "5+ years of Python", "Master’s in Engineering", etc.). Be precise and list the requirements explicitly.
2.  **Resume Comparison:** Meticulously check the resume for explicit evidence for each critical requirement. Do not infer or assume any skills or experiences that are not explicitly stated in the resume.
3.  **Score Calculation (Chain of Thought):**
    *   **Initial Assessment:** Start with a baseline score of 100.
    *   **Weighted Categories:** Evaluate the candidate against the job description's requirements in three weighted categories: Skills (60%), Experience (30%), and Education (10%).
    *   **Apply Penalties:** For each missing critical requirement, subtract a significant number of points. Use a consistent penalty score for each missing requirement based on its importance. A candidate missing a core skill or the required years of experience cannot receive a high score. The final score must be a realistic measure of their current fit. Provide a clear explanation of how the final score was calculated.
    *   **Final Score:** The resulting number is the `match_percentage`.
4.  **Gap Analysis:** In the `weaknesses` section, clearly and neutrally state which key skills or experiences are missing. Be specific and list the missing requirements explicitly.
5.  **Summary & Recommendations (Constructive Tone):**
    *   In `candidate_summary`, write a 2-3 sentence summary of the candidate’s fit. Be balanced, acknowledging strengths while noting gaps.
    *   In `recommendations`, provide actionable, encouraging advice. Suggest specific areas for improvement and potential resources (like online courses) to help the candidate become a stronger applicant in the future.
6.  **Strict Objectivity:** Use only information present in the resume and job description. Do not infer, assume, or invent any details.
7.  **JSON Output:** Your final output MUST be a valid JSON object that conforms to the schema provided in the format instructions. Do not include any markdown formatting (e.g., ```json) around the JSON object.

**Input Data:**

**Job Description:**
---
{job_description}
---

**Resume Text:**
---
{resume_text}
---

{format_instructions}
        """

        prompt = PromptTemplate(
            template=prompt_template,
            input_variables=["resume_text", "job_description"],
            partial_variables={"format_instructions": self.parser.get_format_instructions()},
        )

        # The LangChain Expression Language (LCEL) chain pipes the components together.
        # 1. The prompt is formatted with the input variables.
        # 2. The formatted prompt is sent to the LLM.
        # 3. The LLM's output is parsed by the JSON parser into a Pydantic object.
        chain = prompt | self.llm | self.parser

        try:
            logger.info("Invoking LLM chain for analysis.")
            response = chain.invoke(
                {"resume_text": resume_text_clean, "job_description": job_description_clean}
            )
            # The parser is configured to return a Pydantic object directly.
            return response
        except LangChainException as e:
            logger.error(f"Error generating structured response from the LLM: {e}")
            return None
        except Exception as e:
            logger.exception(f"An unexpected error occurred during LLM invocation: {e}")
            return None
