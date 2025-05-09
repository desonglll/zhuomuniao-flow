

```
docker save -o flask-react-app.tar flask-react-app

docker load -i flask-react-app.tar

docker run -p 8080:8080 -p 8000:8000 flask-react-app

```