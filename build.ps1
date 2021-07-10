poetry export --without-hashes > requirements.txt
docker build --tag fastapi-wake-on-lan:dev .
docker run --rm -it fastapi-wake-on-lan:dev