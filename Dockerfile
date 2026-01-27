FROM python:3.11-slim

WORKDIR /action

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy action files
COPY entrypoint.sh .
COPY scan.py .

# Make entrypoint executable
RUN chmod +x entrypoint.sh

ENTRYPOINT ["/action/entrypoint.sh"]
