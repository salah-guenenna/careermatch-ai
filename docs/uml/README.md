# UML CareerMatch AI

Les diagrammes sont écrits en PlantUML afin de rester modifiables et versionnables.

## Fichiers

- `01-use-case.puml` : acteurs et fonctionnalités principales.
- `02-class-model.puml` : modèle métier et relations.
- `03-analysis-sequence.puml` : séquence de création d'une analyse.
- `04-component.puml` : composants frontend, API, services, IA et base.
- `05-deployment.puml` : déploiement Docker local ou production.
- `06-package.puml` : organisation des packages backend et frontend.

## Générer les images

Avec PlantUML installé :

```bash
plantuml docs/uml/*.puml
```

Ou utilisez une extension PlantUML dans VS Code. Les fichiers `.puml` constituent les sources de référence ; les PNG/SVG générés peuvent être ajoutés aux livrables si nécessaire.

