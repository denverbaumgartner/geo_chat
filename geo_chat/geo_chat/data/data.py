import logging 

from subgrounds.pagination import ShallowStrategy
from subgrounds import Subgrounds, Subgraph, SyntheticField

logger = logging.getLogger(__name__)

# Stop subgrounds from logging kak
logging.getLogger("subgrounds").setLevel(logging.WARNING)

class GeoData: 
    """This class represents the Geo subgraph, and it utilized to collect data from the Geo protocol
    
    :param url: The URL to be used to query data from the Geo sugraph
    :type url: str
    """

    


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

'''
{
  geoEntities {
    id
    name
    entityOf { # these are triples associated with an entity
      id
      attribute {
        id
        name
      }
      # etc.
    }
  }
}
'''


''' example query where we get an entity, its attributes (tubples), and their attributes (tuples). this allows us to collect a description of the entity, and a description of its attributes. 
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
        entityOf {
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
'''