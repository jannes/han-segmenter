FROM tiangolo/uvicorn-gunicorn:python3.8

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install pkuseg
COPY . /app