docker build -t pythonselenium -f Dockerfile .
docker tag pythonselenium bolferdocker/pythonselenium:latest
docker push bolferdocker/pythonselenium:latest
