# Bonn Stock Exchange

Realisiert:

## Contributors

- Daniil (CTO): Datentypen, dokumentation
- Felix (CEO): Tests, Exceptions, Fehlerbehebung
- Mohammed (CUO - Chief UML Officer):UML 

## Credits
- Sir Tim Berners-Lee: Thanks for the Internet
- Felix Boes: Dessen Vorlesungen die Grundlage für dieses Projekt bilden.

## Setup for Server/Client
Install Requirements:
```shell

pip install -r requirements.txt
```

```shell
cd server &&
cmake -S . -B build/ &&
cmake --build build/ &&
cmake --install build
```

### Run Server
```shell
cd server/extra/
uvicorn server:app --reload
```


### Run Client
`python3 client/src/gui.py`




