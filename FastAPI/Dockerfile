# Use Official Python Image
FROM python:3.11.13-slim

# Set Working Directory
WORKDIR /app

# Copy Project Files
COPY . .

# Installing dependencies
RUN python -m pip install --no-cache-dir -r requirements.txt

# Expose Port
EXPOSE 8000

# Start FastAPI App
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]