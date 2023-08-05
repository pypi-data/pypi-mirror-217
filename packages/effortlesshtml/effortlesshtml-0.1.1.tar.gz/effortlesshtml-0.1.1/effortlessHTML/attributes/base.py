from typing import Any


class HTMLAttribute:
    def __init__(self, attribute_name: str, attribute_value: Any):
        self.attribute_name = attribute_name
        self.attribute_value = attribute_value

    def serialize(self) -> str:
        serializer = getattr(
            self, f"serialize_{self.attribute_name}", self.serialize_other
        )
        return serializer()

    def serialize_style(self) -> str:
        serialized_values = ""
        for key, val in self.attribute_value.items():
            serialized_values += f"{key}:{val};"
        return f'{self.attribute_name}="{serialized_values}"'

    def serialize_other(self) -> str:
        return f'{self.attribute_name}="{str(self.attribute_value)}"'
