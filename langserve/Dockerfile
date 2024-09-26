# Use a Python slim image
FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Copy all files from the current directory to the container
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port that LangServe will run on
EXPOSE 5001

# Run the LangServe app
CMD ["python", "langserve_service.py"]