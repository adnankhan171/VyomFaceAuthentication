# Use a minimal Python image to reduce size
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Set default environment variables
ENV FACE_MATCH_THRESHOLD=16.0  

# Copy requirements and install dependencies
COPY requirements.txt .  
RUN pip install --no-cache-dir -r requirements.txt  

# ✅ Preload the Facenet512 model to cache it in the image
RUN python -c "from deepface import DeepFace; DeepFace.build_model('Facenet512')"

# Copy application files
COPY . .  

# Expose the port (for local testing)
EXPOSE 8080     

# Start the app with Gunicorn, binding to dynamic PORT
CMD ["python", "app.py"]
