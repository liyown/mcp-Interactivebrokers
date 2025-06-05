from ib_async import AccountValue
from typing import List, Generic, TypeVar
import json

T = TypeVar("T")


def format_account_summary(account_summary: List[AccountValue]):
    """
    格式化账户摘要 为dict:
    {
        "field":{
            "value": "value",
            "currency": "currency",
            "description": {
                "en": "description",
                "zh": "描述"
            }
        }
    }
    """
    formatted_account_summary = {}

    with open("utils/account_value_map.json", "r", encoding="utf-8") as f:
        account_summary_map = json.load(f)

    for field in account_summary:
        formatted_account_summary[field.tag] = {
            "value": field.value,
            "currency": field.currency,
            "description": account_summary_map[field.tag],
        }

    return formatted_account_summary


class ApiResponse(Generic[T]):
    def __init__(self, data: T, code: int, message: str):
        self.data = data
        self.code = code
        self.message = message

    def to_dict(self):
        return {"data": self.data, "code": self.code, "message": self.message}

    def to_json(self):
        return json.dumps(self.to_dict())

    @staticmethod
    def success(data: T):
        return ApiResponse(data, 200, "success")

    @staticmethod
    def error(message: str):
        return ApiResponse(None, 500, message)

    def sse_encode(self):
        return f"data: {self.to_json()}\n\n"
