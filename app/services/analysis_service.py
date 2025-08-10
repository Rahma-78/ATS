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
from functools import lru_cache

from app.api.schemas import AnalysisResult

class ATSAnalyzer:
    """
    Handles text extraction from files and AI-powered analysis using a structured output approach.
    """

    def __init__(
        self,
        groq_api_key: str,
        model_name: str,
        temperature: float = 0.0,
        model_kwargs: Optional[dict] = None,
    ):
        """
        Initializes the analyzer with the Groq LLM and a JSON output parser.
        """
        if not groq_api_key:
            raise ValueError("GROQ_API_KEY cannot be empty.")

        if model_kwargs is None:
            model_kwargs = {"response_format": {"type": "json_object"}}

        self.llm = ChatGroq(
            api_key=SecretStr(groq_api_key),
            model=model_name,
            temperature=temperature,
            model_kwargs=model_kwargs,
        )
        self.parser = JsonOutputParser(pydantic_object=AnalysisResult)

    def _clean_text(self, text: str) -> str:
        """A private helper method to clean text."""
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'[^\x00-\x7F]+', '', text)  # Remove non-ASCII characters
        return text.strip()

    @lru_cache(maxsize=128)
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
        max_len = 3000
        resume_text_clean = self._clean_text(resume_text)[:max_len]
        job_description_clean = self._clean_text(job_description)[:max_len]

        if len(resume_text_clean) < 100:
            logging.error("Extracted resume text is too short. The file may be empty or image-based.")
            return None
        if len(job_description_clean) < 50:
            logging.error("Job description text is too short. Please provide a detailed job description.")
            return None

        prompt_template = """**Role:** You are an expert AI-powered Applicant Tracking System (ATS) with the persona of a seasoned, insightful, and constructive senior hiring manager. Your goal is to provide a fair, balanced, and helpful analysis.

**Objective:** Analyze the provided resume against the job description and return a structured JSON object with your findings. The analysis must be objective, factual, and strictly based on the text provided.

**Analysis Steps & Tone:**

1.  **Critical Requirements Extraction:** Identify all non-negotiable requirements from the job description (e.g., "5+ years of Python", "Master’s in Engineering", etc.). Be precise and list the requirements explicitly.
2.  **Resume Comparison:** Meticulously check the resume for explicit evidence for each critical requirement. Do not infer or assume any skills or experiences that are not explicitly stated in the resume.
3.  **Score Calculation:**
    *   **Requirement Identification:** Identify a list of key requirements from the job description.
    *   **Evidence-Based Matching:** For each requirement, check the resume for direct evidence.
    *   **Quantitative Scoring:** The `match_percentage` is `(Number of met requirements / Total number of requirements) * 100`. The result must be an integer.
    *   **Explanation:** In the `candidate_summary`, list the requirements and whether they were met.
4.  **Gap Analysis:** In the `weaknesses` section, clearly and neutrally state which key skills or experiences are missing. Be specific and list the missing requirements explicitly.
5.  **Summary & Recommendations (Constructive Tone):**
    *   In `candidate_summary`, write a 2-3 sentence summary of the candidate’s fit. Be balanced, acknowledging strengths while noting gaps.
    *   In `recommendations`, provide actionable, encouraging advice. Suggest specific areas for improvement and potential resources (like online courses) to help the candidate become a stronger applicant in the future.
6.  **Strict Objectivity:** Use only information present in the resume and job description. Do not infer, assume, or invent any details.
7.  **JSON Output:** Your final output MUST be a valid JSON object that conforms to the schema provided in the format instructions.

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

        chain = prompt | self.llm | self.parser

        try:
            response = chain.invoke(
                {"resume_text": resume_text_clean, "job_description": job_description_clean}
            )
            return response
        except LangChainException as e:
            logging.error(f"Error generating structured response from Llama model: {e}")
            return None
        except Exception as e:
            logging.error(f"An unexpected error occurred during LLM invocation: {e}")
            return None
