# Geo Data

This serves as both an overview of data collection from Geo and a primer on the data structure of the system. Geo is structured on triples, below is a brief primer on the subject: 

## Triple Store
A `triple store` is a type of database that is optimized for the storage, retrieval, and querying of triples, a data structure found in semantic web and linked data technologies. Each triple consists of a subject, a predicate, and an object, which together represent a fact or a statement about a resource.

Here's a breakdown of each component of a **triple**:

- **Entity:** This is the entity or resource the triple is describing. It is generally identified using a URI (Uniform Resource Identifier).

- **Attribute:** This represents the relationship or property that links the subject to the object. It is also usually identified using a URI.

- **Value:** This is the value or resource that is linked to the subject by the predicate. It can be another resource identified using a URI, or a literal value like a string, number, or date.

For example, consider the triple:

```
    Entity: http://example.org/people/alice
    Attribute: http://example.org/vocabulary/birthDate
    Value: 1990-01-01
```

This triple represents the fact that `"Alice has a birth date of January 1, 1990"`.

Triple stores are used to manage RDF (Resource Description Framework) data, and they support querying through languages like SPARQL, which allows users to retrieve and manipulate data stored in the triple store.

By storing data as triples, it facilitates a more flexible and semantic approach to data management, allowing for more complex and nuanced queries compared to traditional relational databases. It's particularly useful in applications where data is highly interconnected and the relationships between data points are as important as the data points themselves.

## Geo Subgraph 

According to the Geo team, this is likely to change sometime in November of 23', so for now I am just going to reference the current subgraph [here](https://github.com/geobrowser/geogenesis/tree/master/packages/subgraph) and expand any explanations based upon any learnings going forward. 

## Data Collection

For the sake of getting started, we are going to start very small and gradually grow our dataset. For today, that means we will simply query triples, and filter for attributes labeled `Description`. This will allow us to capture all entities and their associated `description` attributes, similar to what the website is doing [here](https://github.com/geobrowser/geogenesis/blob/3ce65d9108f27a1cd32dae873449caa612ac64ca/apps/web/core/utils/entity/entity.ts#L12).

Going forward, we will want to expand our data collection to not just get the descriptions, but to collect all of the relevant data regarding an attribute (such as where an entity is recorded as the attribute). We can even take this a step further, and collect the triples associated with that entity value (the description being the most relevant piece of information currently). This will provide us a very rich dataset to go off of, where we can collect not just all attribute values associated with an entity, but all of the attribute values associated with the entities attributes. Given the nature of `attention layers`, I believe we can do some very interesting work here that accounts for the context of how far removed a given piece of text is from the target entity during training. An example of a query to do just that for any entity with the name `Subgraph` is below: 

```graphql
{
  geoEntities(where: {name:"Subgraph"}) {
    id
    name
		entityOf {
      attribute {
        id
        name
      }
      valueType
      numberValue
      stringValue
      arrayValue
      entityValue {
        id
        name
        entityOf(where: {attribute_:{name:"Description"}}) {
          attribute {
            id
            name
          }
          valueType
          valueId
          numberValue
          stringValue
          arrayValue
          entity {
            id
            name
          }
        }
      }
    }
  }
}
```