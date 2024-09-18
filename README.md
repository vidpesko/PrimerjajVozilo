# PrimerjajVozilo
Spletna stran za primerjavo rabljenih vozil najdenih na aplikaciji avto.net


### Izbira imena:
    - Carmatica
    - PametnaIzbira *
    - MojNoviAvto *


## Tehnična dokumentacija

### Shranjevanje primerjave v url-u (možnost deljenja primerjave s url)

Ko dodaš novo vozilo v primerjavo, se ti samodejno posodobi url s id-jom vozila:

    1. /primerjaj?vozilo=[ id1 ]
    2. /primerjaj?vozilo=[ id1 ]&vozilo=[ id2 ]


### get-vehicle odgovor:

{
    "id": [avtonetid],
    "required": {
        "name": [name],
        "images": [img1Url, img2Url,...]  # Ce oglas nima slike, bo namesto te slike nek default image (missing)
        "mileage": [mileage],
        "power": [power],
        "firstRegistration": [registration],
        "location": [location],
        "phoneNumber": [number]
    },
    "optional": {
        numOfDoors: {
            humanReadableName: 
        }
    },
    "metadata": {
        "url": [url],
        "updated": [updated]
    }
}