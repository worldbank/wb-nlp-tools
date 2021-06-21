from wb_nlp import dir_manager
from wb_cleaning.extraction import country_extractor as ce


class TestCountryExtractor:
    def test_get_normalized_country_group_name(self):
        code = "ASEAN+COUNTRIES_DATA"
        expected = [
            code,
            "asean+countries_data",
            "ASEAN COUNTRIES_DATA",
            "ASEAN+COUNTRIES DATA",
        ]
        returns = ce.get_normalized_country_group_name(code)

        assert expected == returns

    def test_get_country_name_from_code(self):
        code = "PHL"
        expected = "Philippines"
        returns = ce.get_country_name_from_code(code)

        assert expected == returns

    def test_load_iso3166_3_country_info(self):
        assert isinstance(ce.load_iso3166_3_country_info(), dict)

    def test_load_country_groups_map(self):
        expected = ['BRN', 'KHM', 'IDN', 'LAO',
                    'MYS', 'MMR', 'PHL', 'SGP', 'THA', 'VNM']
        country_groups = ce.load_country_groups_map()

        errors = []

        if not isinstance(country_groups, dict):
            errors.append("load_country_groups_map:: return not dict instance")

        if expected != country_groups.get("ASEAN"):
            errors.append("load_country_groups_map:: country group not found")

        error_string = "\n".join(errors)
        assert not error_string, f"errors in: \n{error_string}"
