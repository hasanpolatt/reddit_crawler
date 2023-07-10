FROM python:3.10.6
WORKDIR /test2

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY main.py .
COPY database.py .

CMD ["python3", "main.py"]