# Base image: python:3.9-slim
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy and install the requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY ./src /app/src
COPY app.py  /app/app.py
COPY .streamlit /app/.streamlit

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run app.py when the container launches
CMD ["streamlit", "run", "app.py", "--server.port", "8000"]