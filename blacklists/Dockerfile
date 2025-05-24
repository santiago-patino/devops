# Usar una imagen base oficial de Python
FROM python:3.9-slim

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar los archivos del proyecto a la carpeta de trabajo
#COPY . /app
COPY Pipfile Pipfile.lock /app/

# Instalar Pipenv
RUN pip install pipenv

# Instalar las dependencias usando Pipenv
#RUN pipenv install
RUN pipenv install --deploy --ignore-pipfile

COPY . /app

#RUN pipenv run python -c "import click; print(click.__version__)"

# Establecer la variable de entorno FLASK_APP
ENV FLASK_APP=./src/main.py

# Exponer el puerto 3000
EXPOSE 3000


# Comando para ejecutar la aplicación Flask
#CMD ["pipenv", "run", "flask", "run", "-h", "0.0.0.0", "-p", "3000"]
CMD ["pipenv", "run", "newrelic-admin", "run-program", "flask", "run", "--host=0.0.0.0", "--port=3000"]
#CMD ["sh", "-c", "NEW_RELIC_CONFIG_FILE=newrelic.ini pipenv run newrelic-admin run-program flask run -h 0.0.0.0 -p 3000"]