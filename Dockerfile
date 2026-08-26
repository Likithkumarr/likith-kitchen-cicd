# Use the official Python 3.12 slim image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container
COPY likith_kitchen/requirements.txt /app/

# Install the Python dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the entire Django project directory into the container
COPY likith_kitchen/ /app/

# Expose port 8000 to allow external connections
EXPOSE 8000

# Command to run the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
