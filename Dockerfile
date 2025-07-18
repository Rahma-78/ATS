FROM python:3.9

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expose the application port (default is 7860)
EXPOSE 7860

HEALTHCHECK --interval=30s --timeout=10s --retries=3 CMD curl -f http://localhost:7860/static/index.html || exit 1

# Command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860", "--limit-concurrency", "10", "--limit-max-requests", "1000"]
