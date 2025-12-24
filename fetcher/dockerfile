FROM python:3.12-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt awslambdaric

# Copy source code
COPY src/ ./src/

# Lambda runtime entrypoint
ENTRYPOINT ["python", "-m", "awslambdaric", "src.handler.handler"]
