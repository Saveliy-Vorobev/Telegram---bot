FROM python:3.10-slim
ENV TOKEN="7629921200:AAG64jccZDjyG2UHpJdFcOgxgCDQWLSIGsI"
COPY . .
RUN pip install -r requirements.txt
ENTRYPOINT ["python", "bot.py"]

