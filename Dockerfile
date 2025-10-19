# Base image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run script
CMD ["python", "main.py"]