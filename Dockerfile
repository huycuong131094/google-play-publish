FROM python:3.10-alpine

WORKDIR /app

COPY requirements.txt .

RUN apk add --no-cache --update python3-dev \
    && pip install --upgrade pip

RUN pip install -r requirements.txt

COPY . .

ENTRYPOINT [ "python", "publish.py" ]