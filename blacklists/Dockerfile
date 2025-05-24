# Usar una imagen base oficial de Python
FROM python:3.9-slim

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar los archivos del proyecto a la carpeta de trabajo
COPY . /app

# Instalar Pipenv
RUN pip install pipenv

# Instalar las dependencias usando Pipenv
RUN pipenv install

# Establecer la variable de entorno FLASK_APP
ENV FLASK_APP=./src/main.py

# Exponer el puerto 3000
EXPOSE 3000

ENV NEW_RELIC_LICENSE_KEY=67e59f83880916ff658834947674e4c5FFFFNRAL
ENV NEW_RELIC_APP_NAME=blacklists-app
ENV NEW_RELIC_LOG=stdout
ENV NEW_RELIC_DISTRIBUTED_TRACING_ENABLED=true
ENV NEW_RELIC_LOG_LEVEL=info
ENV NEW_RELIC_CONFIG_FILE=newrelic.ini

# Comando para ejecutar la aplicación Flask
#CMD ["pipenv", "run", "flask", "run", "-h", "0.0.0.0", "-p", "3000"]

CMD ["sh", "-c", "pipenv run newrelic-admin run-program flask run -h 0.0.0.0 -p 3000"]