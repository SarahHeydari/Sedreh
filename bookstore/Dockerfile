FROM registry.sedrehgroup.ir/python:3.11.1
RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get -y install binutils libproj-dev gdal-bin

RUN apt-get -y update
RUN apt-get -y install cron

# Set the working directory in the container
WORKDIR ./bookstore

# Install dependencies
COPY ./requirements.txt .
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . .

# Expose port 8000 for the application
EXPOSE 8000

# Set environment variables (optional)
ENV PYTHONUNBUFFERD=1

# Run the Django server
#CMD ["python", "manage.py", "runserver", "127.0.0.1:8000"]
CMD ["sh", "entrypoint.sh"]
