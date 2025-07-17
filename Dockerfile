
# Use a Python base image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Create a non-root user
RUN useradd -m -u 1000 user
USER user

# Set environment variables
ENV HOME=/home/user
ENV PATH=$HOME/.local/bin:$PATH

# Copy and install dependencies
COPY --chown=user:user requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Copy the application code
COPY --chown=user:user . .

# Expose the application port (default is 7860)
EXPOSE 7860

# Command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860", "--root-path", "/spaces/Rahma07/ATS"]
