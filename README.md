# Bonn Stock Exchange


## Wenn Database locked. 
- Use 
```shell
fuser path
```
- And kill 
```shell
kill -9 {parameters}
```


## Contributors

- Daniil (CTO): Datentypen, dokumentation
- Felix (CEO): Tests, Exceptions, Fehlerbehebung
- Mohammed (CUO - Chief UML Officer):UML 

## Credits
- Sir Tim Berners-Lee: Thanks for the Internet
- Felix Boes: Dessen Vorlesungen die Grundlage für dieses Projekt bilden.
- Typ, der die DataBank in C++ implementiert hat

## Setup for Server/Client
Install Requirements:
```shell
pip install -r requirements.txt
```

```shell
sudo ./build.sh
```

### Run Server
```shell
cd server/extra/
uvicorn server:app --reload
```


### Run Client

```shell
python3 client/src/client.py
```




