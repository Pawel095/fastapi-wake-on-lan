FROM python:3.9-slim
RUN apt update && apt install inetutils-ping -y
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . /app
EXPOSE 8000
CMD [ "uvicorn","main:app", "--host", "0.0.0.0"]