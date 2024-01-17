# ENT - IUT de Montreuil - API
Gestionnaire d'emploi du temps conçu pour l'IUT de Montreuil

## Installation

### Docker

Lancement du back (DockerFile BACK)
```bash
Docker run -d ismailskr/sae-back:latest
```
Lancement du front (DockerFile FRONT)
```bash
Docker run -d ismailskr/sae-front:latest
```

Docker compose : 
```bash
Docker compose up –build
```


## Architecture du projet

Les routes de l'API sont définies dans le dossier "controller", où la gestion des requêtes HTTP est orchestrée. Simultanément, le dossier "service" abrite les fonctionnalités métier de l'API, établissant une distinction claire entre la gestion des routes et la logique métier.

Quant au dossier "entities", il renferme les modèles SQLAlchemy, consolidant la gestion des entités et de la base de données associée. Ainsi, cette structuration favorise une séparation efficace entre les aspects liés aux routes, aux services et à la gestion des données au sein de l'API.

## 👷  Participants
• [@PriyankSolanki](https://github.com/PriyankSolanki) : Priyank Solanki

• [@stvenchg](https://github.com/stvenchg) : Steven Ching

• [@YanisTTC](https://github.com/YanisTTC) : Yanis Hamani

• [@ecyriaque](https://github.com/ecyriaque) : Emilio Cyriaque

• [@IsmailSKR](https://github.com/IsmailSKR) : Ismaïl Gada
