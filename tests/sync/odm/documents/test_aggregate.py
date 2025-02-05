from pydantic import Field
from pydantic.main import BaseModel

from tests.sync.models import DocumentTestModel


def test_aggregate(documents):
    documents(4, "uno")
    documents(2, "dos")
    documents(1, "cuatro")
    result = DocumentTestModel.aggregate(
        [{"$group": {"_id": "$test_str", "total": {"$sum": "$test_int"}}}]
    ).to_list()
    assert len(result) == 3
    assert {"_id": "cuatro", "total": 0} in result
    assert {"_id": "dos", "total": 1} in result
    assert {"_id": "uno", "total": 6} in result


def test_aggregate_with_filter(documents):
    documents(4, "uno")
    documents(2, "dos")
    documents(1, "cuatro")
    result = (
        DocumentTestModel.find(DocumentTestModel.test_int >= 1)
        .aggregate(
            [{"$group": {"_id": "$test_str", "total": {"$sum": "$test_int"}}}]
        )
        .to_list()
    )
    assert len(result) == 2
    assert {"_id": "dos", "total": 1} in result
    assert {"_id": "uno", "total": 6} in result


def test_aggregate_with_item_model(documents):
    class OutputItem(BaseModel):
        id: str = Field(None, alias="_id")
        total: int

    documents(4, "uno")
    documents(2, "dos")
    documents(1, "cuatro")
    ids = []
    for i in DocumentTestModel.aggregate(
        [{"$group": {"_id": "$test_str", "total": {"$sum": "$test_int"}}}],
        projection_model=OutputItem,
    ):
        if i.id == "cuatro":
            assert i.total == 0
        elif i.id == "dos":
            assert i.total == 1
        elif i.id == "uno":
            assert i.total == 6
        else:
            raise KeyError
        ids.append(i.id)
    assert set(ids) == {"cuatro", "dos", "uno"}


def test_aggregate_with_session(documents, session):
    documents(4, "uno")
    documents(2, "dos")
    documents(1, "cuatro")
    result = DocumentTestModel.aggregate(
        [{"$group": {"_id": "$test_str", "total": {"$sum": "$test_int"}}}],
        session=session,
    ).to_list()
    assert len(result) == 3
    assert {"_id": "cuatro", "total": 0} in result
    assert {"_id": "dos", "total": 1} in result
    assert {"_id": "uno", "total": 6} in result
