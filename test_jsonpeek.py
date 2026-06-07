import jsonpeek


def test_type_names():
    assert jsonpeek.type_name(1) == "int"
    assert jsonpeek.type_name(True) == "bool"
    assert jsonpeek.type_name(1.5) == "float"
    assert jsonpeek.type_name(None) == "null"

def test_schema_of_flat_object():
    assert jsonpeek.schema({"a": 1, "b": "x"}) == {"a": "int", "b": "str"}


def test_schema_of_list_samples_items():
    assert jsonpeek.schema([{"a": 1}, {"a": 2}]) == [{"a": "int"}]

def test_merge_marks_missing_keys_optional():
    merged = jsonpeek.schema([{"a": 1}, {"a": 1, "b": 2}])
    assert merged[0]["b"] == ("int", "optional")
