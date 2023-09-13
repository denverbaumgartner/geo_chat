'''query to return entites and their descriptions
{
  triples(where: {attribute_:{name:"Description"}}) {
    entity {
      name
    }
    attribute {
      name
    }
    stringValue
  }
}
'''