Copy code
#!/bin/bash

# Initialize the database
airflow db init

# Create an admin user
airflow users create \
    --username admin \
    --password admin \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email admin@example.com

# Start the webserver and scheduler
if [ "$AIRFLOW_ENVIRONMENT" = "DEVELOPMENT" ]; then
  airflow webserver --reload-on-plugin-change &
  airflow scheduler --reload-on-plugin-change
else
  airflow webserver &
  airflow scheduler
fi