# Fairoulette

Realisiert:
- GUI mit Knopfen und Wette; Registration GUI
- Sign/Log in Funktionen in Client mir der Aktualisierung von Balance
- Wette mit Sinchranisation
- sqlite: create_user, create_bet; models
- Funktionen in server.py
- Zusammenhang python mit c++
- random(0,36)

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




