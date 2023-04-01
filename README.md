# README

## Descripción del proyecto

Este proyecto utiliza Apache Airflow para leer un archivo CSV y cargar los datos en una base de datos MySQL. El archivo DAG `csv_to_mysql.py` contiene la lógica de lectura del archivo CSV, el monitoreo de cambios en el archivo y la carga de los datos en la base de datos MySQL.

## Requisitos

- Docker y Docker Compose instalados
- Apache Airflow con soporte para MySQL

## Instrucciones de uso

1. Asegúrese de tener instalados Docker y Docker Compose.
2. Utilice el `Dockerfile` proporcionado para construir la imagen de Docker necesaria para ejecutar el proyecto.
3. Utilice `docker-compose.yml` para levantar los servicios necesarios (Apache Airflow, MySQL, etc.).
4. Coloque el archivo CSV con los datos a cargar en la carpeta `data`. El archivo debe llamarse `data.csv`.
5. Inicie el contenedor de Docker y acceda a la interfaz de usuario de Airflow.
6. Active el DAG `csv_to_mysql` y observe cómo se ejecutan las tareas.
7. Una vez finalizado, los datos del archivo CSV deberían cargarse en la base de datos MySQL.

## Estructura del archivo DAG

El archivo DAG `csv_to_mysql.py` define las siguientes tareas y dependencias:

1. `create_table`: Crea la tabla `csv_data` en la base de datos MySQL si no existe.
2. `file_sensor`: Monitorea el archivo CSV y espera a que haya cambios en él.
3. `read_csv_and_load_to_mysql`: Lee el archivo CSV y carga los datos en la base de datos MySQL.

La secuencia de ejecución de las tareas es la siguiente: `create_table` >> `file_sensor` >> `read_csv_and_load_to_mysql`.

## Funciones principales

El archivo DAG contiene las siguientes funciones principales:

- `read_csv`: Lee el archivo CSV y devuelve los datos como una lista de diccionarios.
- `read_csv_and_load_to_mysql`: Llama a la función `read_csv` y luego carga los datos en la base de datos MySQL.
- `load_to_mysql`: Carga los datos en la base de datos MySQL.

## Variables de entorno

El archivo `Dockerfile` define una variable de entorno `AIRFLOW_ENVIRONMENT` que se utiliza para distinguir entre entornos de desarrollo y producción. Por defecto, esta variable está configurada en `DEVELOPMENT`.
