import logging
from typing import Optional, Dict, List, Union

import pandas as pd

from subgrounds import Subgrounds, Subgraph, SyntheticField, FieldPath, Query, Field, ShallowStrategy, LegacyStrategy

logger = logging.getLogger(__name__)

class SubgraphEntity: 
    """Helper object for querying entities from the subgraph
    
    :param subgraph: An initialized subgraph object 
    :type subgraph: subgrounds.Subgraph 
    """

    def __init__(
        self, 
        subgraph: Subgraph,
    ) -> None: 
        
        self.sg = subgraph # TODO: decide if we want to do schema validation as we already handle this within data.py

    ################################################
    # Query Methods                                #
    ################################################

    # def query_as_json

    def query_as_pd(
        self, 
        fields: List[Field | SyntheticField], #TODO: double check this is correct sytax 
        column_names: Optional[Dict[str, str]] = None,
        pagination_strategy: Optional[any] = ShallowStrategy, # TODO: validate, as you can create custom pagination strategies, that any is the best type here
    ) -> Optional[pd.DataFrame]: # TODO: if not return none, change from optional 
        """A method to query the subgraph endpoint for triple entities and return them in a pandas dataframe
        
        :param fields: The field to be returned from the entity
        :par
        """
        
        df = self.subgrounds.query_df(
            fields, 
            pagination_strategy=pagination_strategy # noqa
        )

        if df.empty: 
            return df # TODO: decide if we want to return None, or initialize an empty df with the correct columns 
        
        if column_names:
            df = df.rename(column_names) # TODO: validate this is the correct way to do this 
    
        return df
        
    # def query_as_pl # TODO: decide if it is worth supporting polars by default 

class TripleEntity(SubgraphEntity): 
    """Helper object for querying Triples entities from the subgraph, extends the `SubgraphEntity` class
    
    :param subgraph: An initialized subgraph object 
    :type subgraph: subgrounds.Subgraph 
    """

    def __init__(
        self, 
        subgraph: Subgraph,
    ) -> None: 

        super().__init__(subgraph=subgraph)

        self.triple = self._intialize_triple()

    ################################################
    # Subgraph Objects                             #
    ################################################

    def _intialize_triple(self): 
        """Initialize the Subgraph triple object and add synthetic fields accordingly"""

        triple = self.sg.Triple

        # add any relevant synthetic fields 

        return triple
    
    ################################################
    # Query Constructors                           #
    ################################################

    def build_query(
        self, 
        first: Optional[int] = 1000, # TODO: graph-node default first is typically 1000, if we could dynamically retrieve this value that would be great  
        attribute_name: Optional[str] = None, # TODO: it would be nice to actually pass this as a list, that way we can filter on one, or many, attribute names
    ) -> Query: # TODO: validate this is the correct return type 
        """A method to build the query for the triple entities
        
        :param first: The amount of entities to return, default 1000
        :type first: Optional[int]
        :param attribute_name: The attribute name that you want to filter triples by 
        :type attribute_name: Optional[str]
        """
        
        # construct the triples query 
        triples = self.sg.Query.triples(
            first=first,
            where={"attribute_": {"name": f"{attribute_name}"}} if attribute_name else None # TODO: because subgrounds does not currently permit relative form nested filtering, we must pass the `where` condition in `GraphQL` format, once this is resolved we should update this accordingly
        )                                                                                   # TODO: open a ticket in subgrounds, or track a subgrounds ticket in this repo to update once the issue is resolved    

        return triples
    
    @staticmethod
    def get_fields(
        triples: Query,
    ) -> List[Field | SyntheticField]: #TODO: double check this is correct sytax 
        # TODO: we may want to add in a query validation, this would be in line with the schema validation to ensure the query is for a `Triple`
        """A method to return relevant field paths to be included in the query for the triple entity.
        
        :param triples: The triples query object to be used 
        :type triples: subgrounds.Query
        """

        return [
            triples.entity.name, 
            triples.attribute.name,
            triples.stringValue
        ]
    
    @staticmethod
    def _field_name_corrections() -> Dict[str, str]: 
        """A helper method to reutrn back a dictionary to be used to rename dataframe columns given the class field paths."""

        return {"stringValue": "string_value"}
    
    ################################################
    # Data Cleaning Methods                        #
    ################################################
    
    @staticmethod
    def clean_pd(
        dataframe: pd.DataFrame
    ) -> pd.DataFrame:
        """A Helper method for data cleaning on a triples dataframe"""
        
        dataframe.columns = [col.replace("triples_", "") for col in dataframe.columns]

        return dataframe