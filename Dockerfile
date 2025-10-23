# 1. Use Python 3.11 slim base image for compatibility and small size
FROM python:3.11-slim

# 2. Set working directory
WORKDIR /app

# 3. Install system dependencies needed for building packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        python3-dev \
        gcc \
        libc-dev \
        libffi-dev \
        libssl-dev \
        && pip install --upgrade --no-cache-dir pip setuptools wheel \
        && apt-get clean && rm -rf /var/lib/apt/lists/*

# 4. Copy only requirements first to leverage Docker cache
COPY requirements.txt .

# 5. Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copy the rest of the app code
COPY . .

# 7. Optional: create a non-root user for security
RUN useradd -ms /bin/bash appuser
USER appuser

# 8. Expose port for Flask
EXPOSE 5000

# 9. Set Flask environment variables (optional but good for production)
ENV FLASK_APP=backend_naive_bayes.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=production

# 10. Command to run your Flask app
CMD ["python", "backend_naive_bayes.py"]
