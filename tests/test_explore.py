from pathlib import Path

import bs4
import pytest

from json_explorer.cli import jsonl_iterator
from json_explorer.explore import INDEX, TripleCounter

FIXTURE_DIR = Path(__file__).parent.resolve() / "data"


@pytest.fixture
def example1():
    objects = jsonl_iterator(FIXTURE_DIR / "example1.jsonl")
    return TripleCounter.from_objects(objects)


@pytest.fixture
def example1_render(example1):
    return example1.html()


@pytest.fixture
def example1_soup(example1_render):
    return bs4.BeautifulSoup(example1_render, features="html.parser")


def test_counts_simple(example1):
    # only one type seen for "refresh"
    refresh_types = example1[("refresh",)]
    assert len(refresh_types) == 1

    # the type seen is an int
    assert refresh_types.get("int")

    # only one unique integer value seen
    refresh_int_values = refresh_types["int"]
    assert len(refresh_int_values) == 1

    # the value was always 20, and it was seen three times
    assert refresh_int_values.get(20) == 3


def test_counts_medium(example1):
    # only one type seen for d.rows[*].id
    row_id_types = example1[("d", "rows", INDEX, "id")]
    assert len(row_id_types) == 1

    # the type seen is an int
    assert row_id_types.get("int")

    # there were 89 different unique int values
    row_id_int_values = row_id_types["int"]
    assert len(row_id_int_values) == 89

    # the value 3490233 occurs once
    assert row_id_int_values.get(3490233) == 1


def test_counts_complicated(example1):
    # three different types seen for d.rows[*].stream
    row_stream_types = example1[("d", "rows", INDEX, "stream")]
    assert len(row_stream_types) == 3

    # the types seen are null, object, and array
    assert row_stream_types.get("NoneType")
    assert row_stream_types.get("dict")
    assert row_stream_types.get("list")

    # null occurred 61 times
    assert row_stream_types["NoneType"][None] == 61

    # when it was an array, it was always empty
    row_stream_list_lengths = row_stream_types["list"]
    assert len(row_stream_list_lengths) == 1
    assert row_stream_list_lengths.get(0)

    # when stream was an object, it had between 2 and 7 properties
    row_stream_dict_lengths = row_stream_types["dict"]
    assert min(row_stream_dict_lengths) == 2
    assert max(row_stream_dict_lengths) == 7


def test_render_simple(example1_render):
    assert example1_render.startswith("<!doctype html>")


def test_document_tree(example1_soup):
    # tree exists
    ul = example1_soup.find("ul", {"class": "tree"})
    assert ul

    # has only one root element
    li_list = ul.find_all("li", recursive=False)
    assert len(li_list) == 1

    # this example has three objects, each always with exactly three
    # properties
    root = li_list[0]
    root_text = root.find("summary").find("span", {"class": "type"}).text
    assert root_text == "object 3, always 3 properties"
    assert len(root.find("ul").find_all("li", recursive=False)) == 3


def test_document_dialog_jmespath(example1_soup):
    for jmespath in ["refresh", "d.rows[*].id", "d.rows[*].stream"]:
        dialog = example1_soup.find("dialog", {"id": jmespath})
        assert dialog

        h2 = dialog.find("h2", {"class": "jmespath"})
        assert h2

        assert h2.text.strip() == jmespath
