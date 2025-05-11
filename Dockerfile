FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

VOLUME /app/allure-results

CMD ["pytest", "-v", "--alluredir=./allure-results", "--executor=selenoid", "--browser=chrome", "--browser_version=125.0"]