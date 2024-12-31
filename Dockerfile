# Use an official Python runtime as a parent image
FROM python:3.11-slim


ENV FLASK_APP=turtle_app
ENV FLASK_ENV=development

# Install PostgreSQL development libraries and gcc for building dependencies
RUN apt-get update && \
    apt-get install -y libpq-dev gcc && \
    rm -rf /var/lib/apt/lists/*

# Create a non-root user and set permissions
RUN useradd -r -s /bin/bash dominik

# Set working directory
WORKDIR /turtle_app

# Copy the requirements file and install dependencies globally
COPY ./requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Verify Gunicorn installation
RUN gunicorn --version

# Add the rest of the application files
COPY . /turtle_app/

# Change ownership of the application files to 'dominik'
RUN chown -R dominik:dominik /turtle_app

# Switch to the non-root user 'dominik'
USER dominik

# Expose the port the app will run on
EXPOSE 8000

# CMD to run the app using Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:8000", "run:application"]

