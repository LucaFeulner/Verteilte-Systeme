# Abgabe Verteilte Systeme

## Projektbeschreibung
Dieses Projekt ist eine Flask-basierte Webanwendung, die eine CouchDB-Datenbank verwendet, um Geburtstage von Wissenschaftlern und Forschern zu verwalten.




## Teil 1

Um die Datenbank zu starte führe den folgeneden Befehl im Ordner VerteilteSysteme/birthday-couchdb/ContainerImage aus. Hier wird das benötigte Image aus der Dockerfile erstellt.

```
docker build -t dhbw-couch:1 .
```

Nachdem das Image erfolgreich gebaut wurde, führe folgenden Befehl aus um die Datenbank zu starten.

```
docker run -d -p 5984:5984 --name couchdb dhbw-couch:1
````

Führe nun die Datei app.py aus.

Sollte nun alles geklappt haben, kannst du über den folgenden Befehl über den Microservice die Datenbank abfragen.

````
http://localhost:8001/api/v1/get_data?month=12&day=28
```
Wenn nun kein fehler aufgetreten ist, erhälst du im Browser folgende Ausgabe:

[
  {
    "born": "28.12.1818",
    "name": "Carl Remigius Fresenius",
    "profession": "Chemist"
  },
  {
    "born": "28.12.1903",
    "name": "John von Neumann",
    "profession": "Mathematician, Physicist, Computer Scientist"
  },
  {
    "born": "28.12.1932",
    "name": "Nichelle Nichols",
    "profession": "Actress"
  },
  {
    "born": "28.12.1969",
    "name": "Linus Torvalds",
    "profession": "Software Engineer"
  }
]



## Teil 2

Um das ganze in einem Container laufen zu lassen, führe folgenden Befehl im Verteilte-Systeme Ordner aus:

````
docker-compose up
```


Nun kann der Service extern z.B. über das Terminal mit folgendem Befehl aufgerufen werden:

````
curl "http://localhost:8001/api/v1/get_data?month=12&day=28"
```


## Teil 3
Starte Minikube mit diesem Befehl
```
minikube start
````
Mit diesem Befehl kann der Docker-Client, auf den Docker-Daemon innerhalb des Minikube-Clusters zuzugreifen
```
eval $(minikube docker-env)
```

Führe anschließend die folgenden Befehle aus, um die Images zu bauen. 
```
docker build -t micronetes:1 .
docker build -t dhbw-couch:1 ./birthday-couchdb/ContainerImage
```

Da der befehl davor ausgeführt wurde, sollten die Images direkt im Minikube Docker-Deamon vorhanden sein.
Um da zu überprüfen, führe folgenden Befehl aus:
```
minikube ssh 'docker images'
```

Falls die Images nicht enthalten sind, mit folgendem Befehl hochladen
````
minikube image load <Name des Images>:<tag>
```

Wurden nun alle Befehle erforgreich ausgeführt, führe die nächsten Befehle aus:
```
kubectl apply -f kubernetes/flask_app_deployment.yaml
kubectl apply -f kubernetes/flask_app_service.yaml
kubectl apply -f kubernetes/couchdb_service.yaml   
kubectl apply -f kubernetes/couchdb_deployment.yaml
kubectl apply -f kubernetes/secret.yaml
````

Nun überprüfe mit folgenden Befehlen ob alles korrekt ausgeführt wurde:
```
kubectl get deployments
kubectl get pods
````

kubectl port-forward <podnamen> 8001:8001

Mit diesem befehl kann extern darauf zugegriffen werden:
```
curl -X GET 'http://localhost:8001/api/v1/get_data?month=12&day=28'
```


Sollten Fehler bei den Pods auftreten, mit folgendem Befehl einen Überblick beschaffen:
```
kubectl logs <Podname>
```





