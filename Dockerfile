# Use the base image
FROM python:3.10

# Set the working directory
WORKDIR /app

# Copy project files
COPY . /app


COPY myproject.conf  /etc/myproject.conf

# Add the outer directory to PYTHONPATH
ENV PYTHONPATH=/app

EXPOSE 5000
# Install dependencies
RUN pip install -r requirements.txt

# Command to run the application
CMD ["python", "-m", "crypto_project.coinapp"]
