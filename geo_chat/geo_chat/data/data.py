import json
import logging 
from typing import Optional, Dict, List, Union

import pandas as pd

from subgrounds.pagination import ShallowStrategy
from subgrounds import Subgrounds, Subgraph, SyntheticField

from .helpers import TripleEntity

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

        self.sg = Subgrounds()
        self.geo = self._initialize_subgraph(url=url)

        # intitialize subgraph entities 
        self.triple = TripleEntity(subgraph=self.geo, subgrounds=self.sg)

    def __repr__(self):
        items = ("{}={!r}".format(k, self.__dict__[k]) for k in self.__dict__)
        return "{}({})".format(type(self).__name__, ", ".join(items))

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
                subgraph = self.sg.load_subgraph(url=url)
                break
            except Exception as e:
                logger.debug(f"Exception loading subgraph: {e}")
                continue
                 
        if subgraph is None: 
            raise ValueError(
                f"subgraph_url: {url} failed to load properly"
            )
        # else: 
            # TODO: #3
            # self._validate_schema(url)
        
        return subgraph

    # def _validate_schema(
    #   self, schema_object # TODO: #3
    # )

    ################################################
    # Query Methods                                #
    ################################################

    def query_triples(
        self, 
        first: Optional[int] = 1000000000, 
        attribute_name: Optional[str] = None,
        column_names: Optional[Dict[str, str]] = None,
        return_type: Optional[str] = "pd", 
        pagination_strategy: Optional[any] = ShallowStrategy,
    ) -> Optional[pd.DataFrame]: 
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

        VALID_RETURN_TYPES = {"pd", "json"}
        
        if return_type not in VALID_RETURN_TYPES:
            logger.error(f"Invalid return_type. Accepted values are: {', '.join(VALID_RETURN_TYPES)}")
            return None
        
        query = self.triple.build_query(first=first, attribute_name=attribute_name)
        fields = self.triple.get_fields(triples=query)

        match return_type:
            case "pd":
                data =  self.triple.query_as_pd(
                    fields=fields, 
                    column_names=column_names if column_names else self.triple._field_name_corrections(), 
                    pagination_strategy=pagination_strategy
                )
                return self.triple.clean_pd(data)
            
            case "json": 
                return self.triple.query_as_json(
                    fields=fields, 
                    column_names=column_names if column_names else self.triple._field_name_corrections(), 
                    pagination_strategy=pagination_strategy
                )