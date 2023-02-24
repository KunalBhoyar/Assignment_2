FROM python:3.10.6
# Base docker image of python 3.x

RUN pip install --upgrade pip
# Upgrade pip package

WORKDIR /fastapi
# Change working dir to app

COPY src/ /fastapi

# COPY ../apis.py ../schemas.py ../requirements.txt ../metadata.db ../aws_logging.py /app/

# COPY ../Authentication /app/Authentication

# COPY ../Util/ /app/Util/

ENV JWT_SECRET='damg_7225_big_data'
ENV DbGeo='/fastapi/data/GEOSPATIAL_DATA.db'
ENV DbPath='/fastapi/data'
ENV DbUser='/fastapi/data/USER_DATA.db'

RUN pip install -r /fastapi/fastapi/requirements.txt

EXPOSE 8000
## Expose a port inside the container on which services run
#
#CMD ["gunicorn" ,"-w", "4", "-k", "uvicorn.workers.UvicornWorker" , "--bind", "0.0.0.0:8000", "apis:app"]
CMD ["python3", "/fastapi/fastapi/main.py"]
# gunicorn command to run the service with 4 worker nodes binding localhost/0.0.0.0 on port 8000 refering app inside the main.py