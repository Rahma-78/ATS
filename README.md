:---:
title: Job Application Tool
sdk: docker
sdk_version: "latest"
app_file: app.py
pinned: false
:---:

# ATS Resume Analyzer

This is a simple Applicant Tracking System (ATS) that analyzes a resume against a job description.

## Running the Application

1.  **Build the Docker image:**

    ```bash
    docker build -t ats-app .
    ```

2.  **Run the Docker container:**

    ```bash
    docker run -p 7860:7860 ats-app
    ```

3.  **Access the application:**

    Open your web browser and navigate to `http://localhost:7860`.

    