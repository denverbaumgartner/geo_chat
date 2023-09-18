import json
import logging
from typing import Optional, Dict, List, Union

import pandas as pd

from subgrounds.pagination import ShallowStrategy, LegacyStrategy
from subgrounds import Subgrounds, Subgraph, SyntheticField, FieldPath, query

logger = logging.getLogger(__name__)


class SubgraphEntity:
    """Helper object for querying entities from the subgraph

    :param subgraph: An initialized subgraph object
    :type subgraph: subgrounds.Subgraph
    :param subgrounds: An initialized Subgrounds object
    :type subgrounds: subgrounds.Subgrounds
    """

    def __init__(
        self,
        subgraph: Subgraph,
        subgrounds: Subgrounds,
    ) -> None:
        self.subgraph = subgraph
        self.subgrounds = subgrounds

    def __repr__(self):
        items = ("{}={!r}".format(k, self.__dict__[k]) for k in self.__dict__)
        return "{}({})".format(type(self).__name__, ", ".join(items))

    ################################################
    # Query Methods                                #
    ################################################

    def query_as_json(
        self,
        fields: List[Union[FieldPath, SyntheticField]],
        column_names: Optional[Dict[str, str]] = None,
        pagination_strategy: Optional[any] = ShallowStrategy,
    ) -> Optional[Dict]:
        """A method to query the subgraph endpoint for triple entities and return them in a json format

        :param fields: The field to be returned from the entity
        :type fields: List[Union[subgrounds.FieldPath, subgrounds.SyntheticField]]
        :param column_names: A Dictionary that can be passed in to update column names
        :type column_names: Optional[Dict[str, str]] = None
        :param pagination_strategy: A pagination strategy to be used when querying the subgraph
        :type pagination_strategy:Optional[any] = ShallowStrategy
        """

        data = self.subgrounds.query_json(
            fields, pagination_strategy=pagination_strategy  # noqa
        )

        # Extracting data and restructuring
        restructured_data = []
        for item in data:
            for key, values in item.items():
                for value in values:
                    new_dict = {
                        "entity": value["entity"]["name"],
                        "attribute": value["attribute"]["name"],
                        "stringValue": value["stringValue"],
                    }
                    restructured_data.append(new_dict)

        # Convert restructured data back to JSON format
        try:
            return json.dumps(restructured_data)
        except:
            logger.warning(
                f"Failed when attempting to convert restructured data back to json format"
            )
            return None

    def query_as_pd(
        self,
        fields: List[Union[FieldPath, SyntheticField]],
        column_names: Optional[Dict[str, str]] = None,
        pagination_strategy: Optional[any] = ShallowStrategy,
    ) -> Optional[pd.DataFrame]:
        """A method to query the subgraph endpoint for triple entities and return them in a pandas dataframe

        :param fields: The field to be returned from the entity
        :type fields: List[Union[subgrounds.FieldPath, subgrounds.SyntheticField]]
        :param column_names: A Dictionary that can be passed in to update column names
        :type column_names: Optional[Dict[str, str]] = None
        :param pagination_strategy: A pagination strategy to be used when querying the subgraph
        :type pagination_strategy:Optional[any] = ShallowStrategy
        """

        df = self.subgrounds.query_df(
            fields, pagination_strategy=pagination_strategy  # noqa
        )

        if df.empty:
            return df

        if column_names:
            df = df.rename(columns=column_names)

        return df


class TripleEntity(SubgraphEntity):
    """Helper object for querying Triples entities from the subgraph, extends the `SubgraphEntity` class

    :param subgraph: An initialized subgraph object
    :type subgraph: subgrounds.Subgraph
    :param subgrounds: An initialized Subgrounds object
    :type subgrounds: subgrounds.Subgrounds
    """

    def __init__(
        self,
        subgraph: Subgraph,
        subgrounds: Subgrounds,
    ) -> None:
        super().__init__(subgraph=subgraph, subgrounds=subgrounds)

        self.triple = self._intialize_triple()

    def __repr__(self):
        items = ("{}={!r}".format(k, self.__dict__[k]) for k in self.__dict__)
        return "{}({})".format(type(self).__name__, ", ".join(items))

    ################################################
    # Subgraph Objects                             #
    ################################################

    def _intialize_triple(self):
        """Initialize the Subgraph triple object and add synthetic fields accordingly"""

        triple = self.subgraph.Triple

        # add any relevant synthetic fields

        return triple

    ################################################
    # Query Constructors                           #
    ################################################

    def build_query(
        self,
        first: Optional[int] = 1000,
        attribute_name: Optional[str] = None,  # TODO: #2
    ) -> query:
        """A method to build the query for the triple entities

        :param first: The amount of entities to return, default 1000
        :type first: Optional[int]
        :param attribute_name: The attribute name that you want to filter triples by
        :type attribute_name: Optional[str]
        """

        # construct the triples query
        triples = self.subgraph.Query.triples(
            first=first,
            where={"attribute_": {"name": f"{attribute_name}"}}
            if attribute_name
            else {},  # TODO: #1
        )

        return triples

    @staticmethod
    def get_fields(  # TODO: #4
        triples: query,
    ) -> List[Union[FieldPath, SyntheticField]]:
        """A method to return relevant field paths to be included in the query for the triple entity.

        :param triples: The triples query object to be used
        :type triples: subgrounds.Query
        """

        return [
            triples.entity.name,
            triples.attribute.name,
            triples.stringValue,
        ]

    @staticmethod
    def _field_name_corrections() -> Dict[str, str]:
        """A helper method to reutrn back a dictionary to be used to rename dataframe columns given the class field paths."""

        return {"triples_stringValue": "string_value"}

    ################################################
    # Data Cleaning Methods                        #
    ################################################

    @staticmethod
    def clean_pd(dataframe: pd.DataFrame) -> pd.DataFrame:
        """A Helper method for data cleaning on a triples dataframe"""

        dataframe.columns = [col.replace("triples_", "") for col in dataframe.columns]

        return dataframe
