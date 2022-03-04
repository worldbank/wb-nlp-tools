# pylint: disable=no-name-in-module
# pylint: disable=no-self-argument
import re
import enum
from typing import List
from datetime import date, datetime
from pydantic import BaseModel, Field, validator, AnyUrl
from hashlib import md5
from dateutil import parser

from wb_cleaning.types.metadata_enums import (
    WBAdminRegions,
    Corpus,
    WBDocTypes,
    WBGeographicRegions,
    WBMajorDocTypes,
    WBTopics,
    MajorDocTypes,
    RegionTypes,
    # WBSubTopics,  # Don't normalize subtopics since we don't have a reliable curated list yet.
)


class SortOrder(enum.Enum):
    asc = "ascending"
    desc = "descending"


class SortOn(BaseModel):
    field: str
    order: SortOrder = SortOrder.desc


class CategoricalFields(enum.Enum):
    adm_region = "adm_region"
    corpus = "corpus"
    country = "country"
    doc_type = "doc_type"
    geo_region = "geo_region"
    major_doc_type = "major_doc_type"
    der_regions = "der_regions"
    topics_src = "topics_src"


class CountryCounts(BaseModel):
    country_code: str
    count: int


class TitleStatementModel(BaseModel):
    """This model corresponds to the title_statement field
    in the document_description metadata.
    """

    idno: str = Field(..., description="Unique identifier for the document. Derived identifiers such as `hex_id` will be based on this.")
    title: str = Field(..., description="Title of the document.")
    sub_title: str = Field(None, description="A short subtitle, if available.")
    alternate_title: str = Field(None, description="Any form of the title used as a substitute or alternative to the formal title of the resource.")
    abbreviated_title: str = Field(None, description="Title as abbreviated for indexing or identification.")


class DocumentDescriptionModel(BaseModel):
    """
    Summary of required fields:
        - hex_id
        - int_id
        - corpus
        - filename_original
        - last_update_date
        - path_original
        - title
    """
    id: str = Field(
        ..., description="Unique identifier for the document. Derived identifiers such as `hex_id` will be based on this.")
    hex_id: str = Field(
        ..., description="This id will be the basis for the `int_id` that will be used in the Milvus index.")
    int_id: int = Field(
        ..., description="This will be the id derived from the `hex_id` that will be used in the Milvus index.")

    abstract: str = Field(
        None,
        description="Abstract of the document."
    )
    adm_region: List[str] = Field(
        None, description="List of administrative regions. Example: Africa.")
    app_tag_jdc: bool = Field(
        False, description="Tag associated with documents that belong to the JDC collection.")
    author: List[str] = Field(
        None, description="List of author names.")

    cleaning_config_id: str = Field(
        None,
        description="This corresponds to the configuration ID of the cleaning pipeline that was used to generate the cleaned file in the `path_clean` field.")
    collection: str = Field(
        None, description="")
    corpus: Corpus = Field(
        ..., description="The corpus id of the document source.")
    country: List[str] = Field(
        None, description="List of countries from the source repository, if available.")

    date_published: date = Field(
        None, description="Publication date of the document.")
    der_acronyms: List[dict] = Field(
        None, description="Extracted acronyms from the document.")
    der_countries: dict = Field(
        None, description="Frequency of extracted countries from the document.")
    der_country: List[str] = Field(
        None, description="List of unique country names extracted from the document."
    )
    der_country_counts: dict = Field(
        None, description="Frequency of extracted countries from the document."
    )
    der_country_details: list = Field(
        None, description="Detailed information on extracted countries from the document."
    )
    der_country_groups: List[str] = Field(
        None, description="List of country groups that the country associated with the document belong to."
    )
    der_jdc_data: List[dict] = Field(
        None, description="List of objects corresponding to tags related to JDC and their respective frequency of occurence in the document."
    )
    der_jdc_tags: List[str] = Field(
        None, description="List of tags found in `der_jdc_data`."
    )
    der_language_detected: str = Field(
        None, description="Language detected in the document.")
    der_language_score: float = Field(
        None, description="Confidence score of the detected language.")
    der_raw_token_count: int = Field(
        None, description="Count of raw tokens.")
    der_regions: List[RegionTypes] = Field(
        None, description="List of unique regions corresponding to countries found in the document.")
    der_top_country: str = Field(
        None, description="Country with the highest frequency of mentions in the document."
    )
    der_top_region: str = Field(
        None, description="Region of the `der_top_country`."
    )
    der_clean_token_count: int = Field(
        None, description="Count of cleaned tokens.")
    digital_identifier: str = Field(
        None,
        description="Document digital identifier. For WB documents, use the information from API; for other corpus, use ISBN, or DOI, or other ID if available.")
    doc_type: List[str] = Field(
        None, description="Document type as defined from the source repository.")

    filename_original: str = Field(
        ..., description="Filename of the document without path.")

    geo_region: List[str] = Field(
        None, description="List of geographic regions covered in the document.")

    journal: str = Field(
        None, description="Journal where the document is published.")

    keywords: List[str] = Field(
        None, description="Keywords extracted from source API or page."
    )

    # language_detected -> der_language_detected
    # language_score -> der_language_score

    language_src: str = Field(
        None, description="Language of the document specified in the source repository.")
    last_update_date: datetime = Field(
        datetime.now(), description="Date when the metadata was last updated.")

    major_doc_type: List[MajorDocTypes] = Field(
        None, description="Curated major document type.")

    path_clean: str = Field(
        None, description="Path to the cleaned text.")

    path_original: str = Field(
        ..., description="Path to the raw text.")
    path_pdf_file: str = Field(
        None, description="Path of the scraped PDF file."
    )
    project_id: List[str] = Field(
        None, description="Project id(s) associated with the document."
    )

    title: str = Field(
        ..., description="")
    # tokens -> der_clean_token_count
    topics_src: List[str] = Field(
        None, description="Raw topics extracted from source.")

    url_pdf: AnyUrl = Field(
        None, description="URL to the PDF source.")
    url_txt: AnyUrl = Field(
        None, description="URL to the TXT source.")

    volume: str = Field(
        None, description="Volume of the journal.")

    wb_id: str = Field(
        None, description="World Bank metadata: id")
    wb_lending_instrument: List[str] = Field(
        None, description="World Bank metadata: lending instrument")
    wb_major_theme: List[str] = Field(
        None, description="World Bank metadata: major theme")
    wb_product_line: str = Field(
        None, description="World Bank metadata: product line")
    wb_project_id: List[str] = Field(
        None, description="World Bank metadata: project id")
    wb_sector: List[str] = Field(
        None, description="World Bank metadata: sector")
    wb_subtopic_src: List[str] = Field(
        None, description="World Bank metadata: subtopic")
    wb_theme: List[str] = Field(
        None, description="World Bank metadata: theme")

    year: int = Field(
        None, description="Year the document is published")


class DocumentModel(BaseModel):
    text: str


# Until comma or end of line
REPUBLIC_OF_PATTERN = re.compile(r"(\S+), (Republic of)(,|$)")


def make_list_or_null(value, delimiter):

    value = REPUBLIC_OF_PATTERN.sub(r"\2 \1,", value).strip(",")

    value = sorted(set([v.strip() for v in value.split(delimiter)]))
    if value == ['']:
        value = None

    return value


def pop_get(body, key):
    try:
        value = body.pop(key)
        if value.strip() == "":
            value = None
    except KeyError:
        value = None

    return value


def migrate_nlp_schema(body):
    """This method updates the data under the previous schema into
    the pydantic MetadataModel schema.
    """
    body = dict(body)

    try:
        int(body["_id"], 16)
        hex_id = body["_id"][:15]
    except ValueError:
        hex_id = md5(body['_id'].encode('utf-8')).hexdigest()[:15]

    body["id"] = pop_get(body, "_id")
    body["_id"] = body["id"]

    body["hex_id"] = hex_id
    body["int_id"] = int(body["hex_id"], 16)

    body["abstract"] = pop_get(body, "abstract")
    body["adm_region"] = make_list_or_null(
        body["adm_region"], delimiter=WBAdminRegions.delimiter)
    body["author"] = make_list_or_null(body["author"], delimiter=",")

    body["cleaning_config_id"] = pop_get(body, "cleaning_config_id")
    body["collection"] = pop_get(body, "collection")
    body["corpus"] = body["corpus"].upper()
    body["country"] = make_list_or_null(body["country"], delimiter=",")

    body["date_published"] = (parser.parse(body["date_published"]).date(
    ) if body["date_published"] not in ["", "NaT"] else None)
    body["der_acronyms"] = pop_get(body, "der_acronyms")
    body["der_countries"] = pop_get(body, "countries")
    body["der_language_detected"] = pop_get(body, "language_detected")
    body["der_language_score"] = pop_get(body, "language_score")
    body["der_raw_token_count"] = pop_get(body, "der_raw_token_count")
    body["der_clean_token_count"] = pop_get(body, "tokens")
    body["digital_identifier"] = pop_get(body, "digital_identifier")
    body["doc_type"] = make_list_or_null(
        WBDocTypes.clean(body["doc_type"]).replace(
            "General Economy, Macroeconomics and Growth Study",
            "General Economy; Macroeconomics and Growth Study"
        ).replace(
            'Foreign Trade, FDI, and Capital Flows Study',
            'Foreign Trade; FDI; and Capital Flows Study'
        ).replace(
            "PSD, Privatization and Industrial Policy",
            "PSD; Privatization and Industrial Policy"
        ), delimiter=WBDocTypes.delimiter)

    # body["filename_original"] = pop_get(body, "filename_original")

    body["geo_region"] = make_list_or_null(
        body["geo_region"], delimiter=WBGeographicRegions.delimiter)

    body["journal"] = pop_get(body, "journal")

    body["language_src"] = pop_get(body, "language_src")
    body["last_update_date"] = datetime.now()

    body["major_doc_type"] = make_list_or_null(
        body["major_doc_type"], delimiter=WBMajorDocTypes.delimiter)

    body["path_clean"] = pop_get(body, "path_clean")
    # body["path_original"] = pop_get(body, "path_original")

    # body["title"] = pop_get(body, "path_original")
    body["topics_src"] = make_list_or_null(
        body["topics_src"].replace(
            "Health, Nutrition and Population",
            "Health; Nutrition and Population"
        ),
        delimiter=WBTopics.delimiter)

    body["url_pdf"] = pop_get(body, "url_pdf")
    body["url_txt"] = pop_get(body, "url_txt")

    body["volume"] = pop_get(body, "volume")
    body["wb_id"] = pop_get(body, "wb_id")
    body["wb_lending_instrument"] = [pop_get(body, "wb_lending_instrument")]
    body["wb_major_theme"] = [pop_get(body, "wb_major_theme")]
    body["wb_product_line"] = pop_get(body, "wb_product_line")
    body["wb_project_id"] = [pop_get(body, "wb_project_id")]
    body["wb_sector"] = [pop_get(body, "wb_sector")]
    body["wb_subtopic_src"] = make_list_or_null(
        body["wb_subtopic_src"], delimiter=",")
    body["wb_theme"] = [pop_get(body, "wb_theme")]

    body["year"] = pop_get(body, "year")

    return body


def make_metadata_model_from_nlp_schema(body):
    body = migrate_nlp_schema(body)

    return MetadataModel(**body)

# e = nlp_coll.find({"path_original": {"$nin": ["", None]}})
# for ix, ee in enumerate(e):
#     try:
#         metadata.make_metadata_model_from_nlp_schema(ee)
#     except Exception as exc:
#         errors = exc.raw_errors

#         for n1 in errors:
#             for n2 in n1:
#                 field_name = n2.loc_tuple()[0]

#                 if field_name != "doc_type":
#                     raise(exc)


# e = nlp_coll.find({"path_original": {"$nin": ["", None]}})
# for ix, ee in enumerate(e):
#     metadata.make_metadata_model_from_nlp_schema(ee)
#     try:
#         metadata.make_metadata_model_from_nlp_schema(ee)
#     except Exception as exc:
#         errors = exc.raw_errors

#         for n1 in errors:
#             for n2 in n1:
#                 field_name = n2.loc_tuple()[0]

#                 if field_name != "doc_type":
#                     raise(exc)
