# Use the official Python base image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the container
COPY ./app/requirements.txt /app/requirements.txt

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Uvicorn
RUN pip install uvicorn

# Copy the FastAPI application code to the container
COPY ./app/main.py /app/main.py

# Copy the models to the container
COPY ./model /app/model

# Expose the port on which the FastAPI application runs (default is 8000)
EXPOSE 8000

# Run the FastAPI application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]