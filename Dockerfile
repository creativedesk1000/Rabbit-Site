# Use Python slim image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy all project files
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir flask flask_sqlalchemy

# Expose Flask default port
EXPOSE 5000

# Run the app
CMD ["python", "app.py"]
