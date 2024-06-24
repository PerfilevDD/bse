# Bonn Stock Exchange

## Währung:
- FRC - FairCoin
- POEUR - POOSE-Euro

## TODO:
- Balance an client auto aktulisieren (vlt mit Websocket (wie?))
- Orders aus Datenbank entfernen (dafür nur func in c++, die das macht)
- Graphik
- Testen mit zwei user
- ???

## !! Wenn Database locked. 
- Use 
```shell
fuser path
```
- And kill this bitch
```shell
kill -9 {parameters}
```

## Realisiert:
- Databank
- Client
- Server
## TODO:
- Balance update
- buy/sell func
- ???

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
sudo dnf install sqlite-devel

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
`python3 client/src/gui.py`




