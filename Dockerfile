FROM python:3.12.4-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

COPY ./app .

EXPOSE 5000

CMD ["python", "app.py"]