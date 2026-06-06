import jsonpeek


def test_type_names():
    assert jsonpeek.type_name(1) == "int"
    assert jsonpeek.type_name(True) == "bool"
    assert jsonpeek.type_name(1.5) == "float"
    assert jsonpeek.type_name(None) == "null"

def test_schema_of_flat_object():
    assert jsonpeek.schema({"a": 1, "b": "x"}) == {"a": "int", "b": "str"}
