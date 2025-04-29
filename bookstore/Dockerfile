FROM registry.sedrehgroup.ir/python:3.11.1
RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get -y install binutils libproj-dev gdal-bin
RUN apt-get -y install cron

# Set the working directory
WORKDIR /bookstore

# Copy all project files
COPY . .

# Upgrade pip
RUN python -m pip install --upgrade pip

# Install Python dependencies
RUN pip install -r requirements.txt

# Expose the application port
EXPOSE 8000

# Set environment variables
ENV PYTHONUNBUFFERD=1

# Run the entrypoint script
CMD ["sh", "entrypoint.sh"]
