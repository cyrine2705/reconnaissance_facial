FROM python:3.9-slim-buster

# Install FFmpeg
RUN apt-get update && \
    apt-get install -y ffmpeg

# Install dlib and cmake
RUN apt-get update && \
    apt-get install -y build-essential cmake 

# Set working directory
WORKDIR /face_rec-main

# Copy application code
COPY . /face_rec-main

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Start the application
CMD ["python", "web_service.py"]
