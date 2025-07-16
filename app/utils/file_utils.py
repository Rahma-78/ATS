# -*- coding: utf-8 -*-
"""
Utility functions for file operations.
"""

import logging
import os
from typing import Optional
import io
from pypdf import PdfReader


def extract_text_from_pdf(file_stream: io.BytesIO) -> Optional[str]:
    """Extracts text content from a PDF file stream."""
    try:
        reader = PdfReader(file_stream)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        logging.error(f"Failed to extract text from PDF stream: {e}")
        return None



def extract_text(file_content: bytes, filename: str) -> Optional[str]:
    """
    Extracts text from file content, supporting PDF.

    Args:
        file_content: The content of the file in bytes.
        filename: The name of the file.

    Returns:
        The extracted text as a string, or None on failure.
    """
    _, extension = os.path.splitext(filename)
    extension = extension.lower()

    if extension == ".pdf":
        text = extract_text_from_pdf(io.BytesIO(file_content))
   
    else:
        logging.error(f"Unsupported file type: {extension}")
        return None

    if not text:
        return None

    # Clean up excessive whitespace from extracted text
    import re
    text = re.sub(r'\s+', ' ', text)
    return text.strip()
