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

    def test_get_country_code_from_name(self):
        name = "Philippines"
        expected = "PHL"

        returns = ce.get_country_code_from_name(name)

        assert expected == returns

    def test_replace_country_group_names(self):
        txt = "countries in asean"
        expected = "countries in ASEAN"

        returns = ce.replace_country_group_names(txt)

        assert expected == returns

    def test_replace_countries(self):
        txt = "countries in philippines"

        # Note the trailing space after PHL
        expected = f"countries in {ce.anchor_code}{ce.DELIMITER}PHL "

        returns = ce.replace_countries(txt)

        assert expected == returns

    def test_get_country_counts_regions(self):
        counts = dict(PHL=20)
        expected = ["East Asia & Pacific"]
        returns = ce.get_country_counts_regions(counts)

        assert expected == returns

    def test_get_country_counts_regions_None(self):
        assert ce.get_country_counts_regions(None) is None

    def test_get_region_countries_None(self):
        assert ce.get_region_countries(None) is None

    def test_get_region_countries(self):
        region = ["South Asia"]
        expected = ['Afghanistan', 'Bangladesh', 'Bhutan',
                    'India', 'Maldives', 'Nepal', 'Pakistan', 'Sri Lanka']

        returns = ce.get_region_countries(region)

        assert expected == returns

    def test_get_region_countries_not_sorted(self):
        region = ["South Asia"]
        expected = ['Maldives', 'Bangladesh', 'Sri Lanka', 'Afghanistan', 'Bhutan',
                    'India', 'Nepal', 'Pakistan', ]

        returns = ce.get_region_countries(region)

        assert sorted(expected) == returns
