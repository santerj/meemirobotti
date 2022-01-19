FROM python:3.9-slim

# ensure dependencies
COPY requirements.txt /tmp/
RUN pip install --upgrade pip 
RUN pip install --no-cache-dir --requirement /tmp/requirements.txt

# start application
COPY source/* /opt
WORKDIR /opt
CMD ["python", "/opt/main.py"]

