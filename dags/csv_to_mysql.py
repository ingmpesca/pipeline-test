import os
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.providers.mysql.operators.mysql import MySqlOperator
from airflow.providers.mysql.hooks.mysql import MySqlHook
from airflow.sensors.filesystem import FileSensor
from datetime import datetime, timedelta
import csv
import logging
import traceback


create_table_sql = '''
CREATE TABLE IF NOT EXISTS csv_data (
    order_number VARCHAR(255) NULL,
    order_status VARCHAR(255) NULL,
    customer_email VARCHAR(255) NULL,
    preferred_delivery_date DATE NULL,
    preferred_delivery_hours VARCHAR(255) NULL,
    sales_person VARCHAR(255) NULL,
    notes TEXT NULL,
    address VARCHAR(255) NULL,
    neighbourhood VARCHAR(255) NULL,
    city VARCHAR(255) NULL,
    creation_date DATE NULL,
    source VARCHAR(255) NULL,
    warehouse VARCHAR(255) NULL,
    shopify_id VARCHAR(255) NULL,
    sales_person_role VARCHAR(255) NULL,
    order_type VARCHAR(255) NULL,
    is_pitayas VARCHAR(255) NULL,
    discount_applications VARCHAR(255) NULL,
    payment_method VARCHAR(255) NULL
);
'''

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 3, 30),
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG(
    'csv_to_mysql',
    default_args=default_args,
    description='Reads CSV file and updates MySQL database',
    schedule_interval='*/1 * * * *'
)

current_directory = os.path.dirname(os.path.abspath(__file__))

def read_csv(csv_file_path):

    csv_file_path = os.path.join(current_directory, '..', 'data', 'data.csv')

    try:
        with open(csv_file_path, 'r') as f:
            # Move the file pointer to the last processed position
            reader = csv.DictReader(f)

            # Process CSV rows
            data = []
            for row in reader:
                # Convert empty date strings to None
                row['preferred_delivery_date'] = row['preferred_delivery_date'] or None
                logging.info("Row: {}".format(row))
                data.append(row)

    except FileNotFoundError:
        logging.error("CSV file not found: {}".format(csv_file_path))
    except Exception as e:
        logging.error("Error while reading CSV file")
        logging.error(traceback.format_exc())
    return data



def read_csv_and_load_to_mysql(csv_file_path):
    # Leemos el archivo CSV
    data = read_csv(csv_file_path)
    
    # Cargamos los datos en MySQL
    load_to_mysql(csv_file_path, data)


def load_to_mysql(csv_file_path, data):
    try:
        # Get the MySQL connection details
        mysql_hook = MySqlHook(mysql_conn_id='mysql_local')
        conn = mysql_hook.get_conn()

        # Execute the SELECT statement to check which rows already exist in MySQL database
        with conn.cursor() as cursor:
            select_stmt = "SELECT order_number FROM csv_data"
            cursor.execute(select_stmt)
            existing_rows = cursor.fetchall()

        # Convert existing rows to a set for faster lookup
        existing_rows_set = set(row[0] for row in existing_rows)

        # Append the new rows to the inserts list if they don't already exist in MySQL database
        inserts = []
        for row in data:
            if row['order_number'] not in existing_rows_set:
                columns = ', '.join(row.keys())
                values = ', '.join(["'" + value.replace("'", "''") + "'" if value is not None else 'NULL' for value in row.values()])
                insert_stmt = f"INSERT INTO csv_data ({columns}) VALUES ({values})"
                inserts.append(insert_stmt)

        # Execute the INSERT statements to add new rows to MySQL database
        with conn.cursor() as cursor:
            for insert_stmt in inserts:
                cursor.execute(insert_stmt)
            conn.commit()

    except Exception as e:
        logging.exception("Error while loading data to MySQL")

with dag:


    # Create table if not exists
    create_table = MySqlOperator(
        task_id='create_table',
        mysql_conn_id='mysql_local',
        sql=create_table_sql,
        dag=dag
    )
    current_directory = os.path.dirname(os.path.abspath(__file__))
    # Define the path to the CSV file
    csv_file_path = os.path.join(current_directory, '..', 'data', 'data.csv')

    # Monitor changes to the CSV file
    file_sensor = FileSensor(
        task_id='file_sensor',
        filepath=csv_file_path,
        fs_conn_id='local_filesystem',
        poke_interval=10,
        dag=dag
    )

    read_csv_and_load_to_mysql_task = PythonOperator(
        task_id='read_csv_and_load_to_mysql',
        python_callable=read_csv_and_load_to_mysql,
        op_args=[csv_file_path],
        dag=dag,
    )

    create_table >> file_sensor >> read_csv_and_load_to_mysql_task

