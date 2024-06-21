# Bonn Stock Exchange SERVER


## Contributors

- Daniil (CTO): Datentypen, dokumentation
- Felix (CEO): Tests, Exceptions, Fehlerbehebung
- Mohammed (CUO - Chief UML Officer):UML 

## Credits
- Sir Tim Berners-Lee: Thanks for the Internet
- Felix Boes: Dessen Vorlesungen die Grundlage für dieses Projekt bilden.

## Setup
```shell
cmake -S . -B build/ &&
cmake --build build/ &&
cmake --install build
```

### Run Server
```shell
cd extra/
uvicorn server:app --reload
```


