# Geo Data

This serves as both an overview of data collection from Geo and a primer on the data structure of the system. Geo is structured on triples, below is a brief primer on the subject: 

## Triple Store
A `triple store` is a type of database that is optimized for the storage, retrieval, and querying of triples, a data structure found in semantic web and linked data technologies. Each triple consists of a subject, a predicate, and an object, which together represent a fact or a statement about a resource.

Here's a breakdown of each component of a **triple**:

- **Subject:** This is the entity or resource the triple is describing. It is generally identified using a URI (Uniform Resource Identifier).

- **Predicate:** This represents the relationship or property that links the subject to the object. It is also usually identified using a URI.

- **Object:** This is the value or resource that is linked to the subject by the predicate. It can be another resource identified using a URI, or a literal value like a string, number, or date.

For example, consider the triple:

```
    Subject: http://example.org/people/alice
    Predicate: http://example.org/vocabulary/birthDate
    Object: 1990-01-01
```

This triple represents the fact that `"Alice has a birth date of January 1, 1990"`.

Triple stores are used to manage RDF (Resource Description Framework) data, and they support querying through languages like SPARQL, which allows users to retrieve and manipulate data stored in the triple store.

By storing data as triples, it facilitates a more flexible and semantic approach to data management, allowing for more complex and nuanced queries compared to traditional relational databases. It's particularly useful in applications where data is highly interconnected and the relationships between data points are as important as the data points themselves.

## Geo Subgraph 

According to the Geo team, this is likely to change sometime in November of 23', so for now I am just going to reference the current subgraph [here](https://github.com/geobrowser/geogenesis/tree/master/packages/subgraph) and expand any explanations based upon any learnings going forward. 