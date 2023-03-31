FROM python:3.8-slim-buster

# Install dependencies
RUN pip install --no-cache-dir apache-airflow[mysql]==2.5.2 apache-airflow-providers-ftp

# Set the working directory
WORKDIR /usr/local/airflow

# Copy the DAG file to the working directory
COPY csv_to_mysql.py .

# Copy the entrypoint script to the working directory
COPY entrypoint.sh .

# Set the entrypoint script as executable
RUN chmod +x entrypoint.sh

# Set the entrypoint command
ENTRYPOINT ["./entrypoint.sh"]

# Set environment variable for Airflow environment
ENV AIRFLOW_ENVIRONMENT=DEVELOPMENT