FROM  python:3

WORKDIR /./

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["cd src", "python3 coderbot.py function.py bot.py redditAPI.py"]
