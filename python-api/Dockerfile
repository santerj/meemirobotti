FROM python:3.10-slim

# ensure dependencies
COPY requirements.txt /tmp/
RUN pip install --upgrade pip 
RUN pip install --no-cache-dir --requirement /tmp/requirements.txt

# start application
COPY source/* /opt
WORKDIR /opt
EXPOSE 80/tcp
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]

