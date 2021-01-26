FROM python:3.8.6

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install pkuseg
COPY . /app
CMD [ "gunicorn", "-w", "3", "-b", "0.0.0.0:8000", "main:server" ]
