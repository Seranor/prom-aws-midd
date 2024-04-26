FROM python:3.11.3

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

CMD ["/bin/bash","-c","python main.py"]