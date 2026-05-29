import pytest

from schema_validator import validate_schema
from schemas import STATUS_SCHEMA


def test_status_schema_accepts_success_response():
    validate_schema(
        {
            "code": 10000,
            "msg": "success",
            "request_id": "smoke-request-id",
        },
        STATUS_SCHEMA,
        path="status",
    )


def test_schema_validator_allows_missing_optional_fields():
    validate_schema(
        {"name": "SeaHot"},
        {"name": str, "avatar?": str},
    )


def test_schema_validator_rejects_wrong_fixed_value():
    with pytest.raises(AssertionError, match="status.code"):
        validate_schema(
            {
                "code": 50000,
                "msg": "success",
                "request_id": "smoke-request-id",
            },
            STATUS_SCHEMA,
            path="status",
        )
