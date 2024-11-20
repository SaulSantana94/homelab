docker build -t pythonselenium -f Dockerfile .
docker tag pythonselenium bolferdocker/pythonselenium:1.0.2
docker push bolferdocker/pythonselenium:1.0.2
