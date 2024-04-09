FROM  python:3

WORKDIR .

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
RUN rm .env
WORKDIR src

CMD ["python3", "coderbot.py"]
