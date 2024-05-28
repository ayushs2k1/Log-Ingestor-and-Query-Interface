# Use the official Python image as base
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files
COPY . .

# Adjust the port number 
EXPOSE 8501


# Adjust the command based on actual application entry points
CMD ["streamlit", "run", "dashboard.py"]
