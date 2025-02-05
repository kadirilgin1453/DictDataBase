import dictdatabase as DDB
from dictdatabase import io_safe
import pytest
import json


def test_read():
    # Elicit read error
    DDB.config.use_orjson = True
    with pytest.raises(json.decoder.JSONDecodeError):
        with open(f"{DDB.config.storage_directory}/corrupted_json.json", "w") as f:
            f.write("This is not JSON")
        io_safe.read("corrupted_json")


def test_partial_read():
    assert io_safe.partial_read("nonexistent", key="none") is None


def test_write():
    with pytest.raises(TypeError):
        io_safe.write("nonexistent", lambda x: x)


def test_delete():
    DDB.at("to_be_deleted").create()
    DDB.at("to_be_deleted").delete()
    assert DDB.at("to_be_deleted").read() is None
