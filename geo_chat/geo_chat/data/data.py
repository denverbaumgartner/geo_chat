import json
import logging 
from typing import Optional, Dict, List, Union

import pandas as pd

from subgrounds.pagination import ShallowStrategy
from subgrounds import Subgrounds, Subgraph, SyntheticField

from helpers import TripleEntity

logger = logging.getLogger(__name__)

# Stop subgrounds from logging kak
logging.getLogger("subgrounds").setLevel(logging.WARNING)

class GeoData: 
    """This class represents the Geo subgraph, and it utilized to collect data from the Geo protocol
    
    :param url: The URL to be used to query data from the Geo sugraph
    :type url: str
    """

    def __init__(
        self, 
        url: str,
    ) -> None:

        self.sg = self._initialize_subgraph(url=url)

        # intitialize subgraph entities 
        self.triple = TripleEntity(self.sg)

    ################################################
    # Subgraph Objects                             #
    ################################################

    def _initialize_subgraph(
        self, url: str, attempts: int = 3
    ) -> Subgraph: 
        """Initialize the subgraph
        
        :param url: The subgraph url
        :type url: str
        :attempts: The number of connection attempts to make 
        :type attempts: int
        :return: A initialized subgraph instance
        :rtype: Subgraph
        """
        
        subgraph = None

        for attempt in range(attempts): 
            try: 
                subgraph = self.subgrounds.load_subgraph(url=url)
                break
            except Exception as e:
                logger.debug(f"Exception loading subgraph: {e}")
                continue
                 
        if subgraph is None: 
            raise ValueError(
                f"subgraph_url: {url} failed to load properly"
            )
        # else: 
            # TODO: add a check to guarantee the schema matches the expected return value 
            # self._validate_schema(url)
        
        return subgraph

    # def _validate_schema(
    #   self, schema_object # TODO: determine how subgrounds stores the schema object and if it is small enough to ship 
    # )

    ################################################
    # Query Methods                                #
    ################################################

    def query_triples(
        self, 
        first: Optional[int] = 1000000000, # TODO: currently, there is no way to get an entity count from the subgraph. if this changes, we should attempt to dynamically set first from that value 
        attribute_name: Optional[str] = None,
        column_names: Optional[Dict[str, str]] = None,
        return_type: Optional[str] = "pd", # TODO: see if there is a clean way to define what string values are accepted 
        pagination_strategy: Optional[any] = ShallowStrategy,
    ) -> Optional[pd.DataFrame]: # TODO: as we add more possible data return types (json next) update this to be a Union
        """A method to query triples entities from the Geo subgraph
        
        :param first: The amount of entities to be returned from the query, defaults to 1,000,000,000
        :type first: Optional[int]
        :param attribute_name: An optional filter on the triple's attribute name
        :type attribute_name: Optional[str]
        :param column_names: An optional param used to rename the column names of the data
        :type column_names: Optional[Dict[str, str]]
        :param return_type: Defines the data structure to be returned, defaults to "pd" (pandas.DataFrame)
        :type return_type: Optional[str]
        :param pagination_strategy: The pagination strategy to be used at time of query, allows for custom pagination strategies to be implemented
        :type pagination_strategy: Optional[any]
        """
        
        query = self.triple.build_query(first=first, attribute_name=attribute_name)
        fields = self.triple.get_fields(query=query)

        # TODO: add a clean way to check that the passed in type is one we support
        # i wonder if using "case" would be a cleaner way to do this? 
        if return_type == 'pd': 
            data =  self.triple.query_as_pd(
                fields=fields, 
                column_names=column_names if column_names else self.triple._field_name_corrections(), 
                pagination_strategy=pagination_strategy
            )
            return self.triple.clean_pd(data)
        else: 
            logger.warning("Currently, this method only supports data returned as a pandas dataframe")


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