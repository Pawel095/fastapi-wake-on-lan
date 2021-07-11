poetry export --without-hashes > requirements.txt
docker build --tag fastapi-wake-on-lan:dev .
docker run --rm -it -p 8000:8000 -v ${pwd}:/app fastapi-wake-on-lan:dev uvicorn main:app --reload --host 0.0.0.0