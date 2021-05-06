# Contribution

Le projet est hébergé sur GitHub

[Visiter GitHub](https://github.com/3liz/qgis-mercicor-plugin/){: .md-button .md-button--primary }

## Code

Le code SQL et Python sont couverts par des tests unitaires utilisant Docker.

[![Tests 🎳](https://github.com/3liz/qgis-mercicor-plugin/actions/workflows/ci.yml/badge.svg)](https://github.com/3liz/qgis-mercicor-plugin/actions/workflows/ci.yml)

```bash
pip install -r requirements/requirements-dev.txt
flake8
make tests
```

## Documentation

La documentation utilise [MkDocs](https://www.mkdocs.org/) avec [Material](https://squidfunk.github.io/mkdocs-material/) :

```bash
pip install -r requirements/requirements-doc.txt
mkdocs serve
```
