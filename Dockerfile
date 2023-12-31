FROM python:3.10-alpine

WORKDIR /code

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . /code/.

CMD [ "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000" ]
