import pandas as pd
from geo_chat.data import GeoData, TripleEntity


class TestGeoData:
    def test_subgraph_initialization(self):
        valid_url = "https://api.thegraph.com/subgraphs/name/baiirun/geo"
        geo = GeoData(url=valid_url)

        # Test GeoData creation
        assert isinstance(geo, GeoData)
        # Test the Subgrounds object was properly created
        assert (
            list(geo.sg.subgraphs.keys())[0]
            == "https://api.thegraph.com/subgraphs/name/baiirun/geo"
        )
        # Test the subgraph object was properly created
        assert geo.geo._url == "https://api.thegraph.com/subgraphs/name/baiirun/geo"
        # Test the triple entity that was created
        assert isinstance(geo.triple, TripleEntity)

        ####################################
        # Query tests                      #
        ####################################
        data_pd = geo.query_triples(first=1, return_type="pd")
        data_json = geo.query_triples(first=1, return_type="json")

        # Test that the pandas dataframe data returned is as expected
        assert isinstance(data_pd, pd.DataFrame)
        assert data_pd.loc[0, "entity_name"] == "Star and crescent"
        assert data_pd.loc[0, "attribute_name"] == "Name"
        assert data_pd.loc[0, "string_value"] == "Star and crescent"
        assert data_pd.columns.to_list() == [
            "entity_name",
            "attribute_name",
            "string_value",
        ]

        # Test that the json data returned is as expected
        assert isinstance(data_json, str)
        assert (
            data_json
            == '[{"entity": "Star and crescent", "attribute": "Name", "stringValue": "Star and crescent"}]'
        )

        data_pd = geo.query_triples(
            first=1, attribute_name="Description", return_type="pd"
        )
        data_json = geo.query_triples(
            first=1, attribute_name="Description", return_type="json"
        )

        # Test that the pandas dataframe data returned is as expected
        assert isinstance(data_pd, pd.DataFrame)
        assert data_pd.loc[0, "entity_name"] == "Law"
        assert data_pd.loc[0, "attribute_name"] == "Description"
        assert data_pd.loc[0, "string_value"] == "A law for individuals to follow"
        assert data_pd.columns.to_list() == [
            "entity_name",
            "attribute_name",
            "string_value",
        ]

        # Test that the json data returned is as expected
        assert isinstance(data_json, str)
        assert (
            data_json
            == '[{"entity": "Law", "attribute": "Description", "stringValue": "A law for individuals to follow"}]'
        )
