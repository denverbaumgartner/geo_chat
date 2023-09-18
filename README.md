# Geo Chat
Exploring the intersections of verifiable data (Geo) &amp; LLMs. Contains data collection methods for interacting with the Geo subgraph. Will contain a training pipeline for fine-tuning LLMs on Geo data. Data collection discussed [here](geo_chat/geo_chat/data/README.md).

## Directory

```
.
├── LICENSE
├── README.md
└── geo_chat
    ├── README.md
    ├── geo_chat
    │   ├── __init__.py
    │   ├── data
    │   │   ├── README.md
    │   │   ├── __init__.py
    │   │   ├── data.py
    │   │   └── helpers
    │   │       ├── __init__.py
    │   │       └── subgraph_types.py
    ├── poetry.lock
    ├── pyproject.toml
    └── tests
        ├── __init__.py
        └── geo_chat_test.py
```

## v0

The initial goal of this repo is to train a model that will take a description as user input, and output which of the entities that input most closely aligns with. The end product is a system that can analyze user input and suggest helpful connections to that input. This could be helpful when a user is entering a new entity into Geo and that entity has the potential to create new tuples with other entities (either as the main entity or the attribute). This could also be helpful for identifying relevant Spaces given a users area of interest. 