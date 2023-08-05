from typing import Any, Optional, Self

from effortlessHTML.attributes import HTMLAttribute


class HTMLElement:
    ELEMENT_TYPE: Optional[str] = None

    def __init__(
        self,
        content: Optional[str] = None,
        *,
        element_type: Optional[str] = None,
        context: Optional[dict] = None,
        children: Optional[list["HTMLElement"] | tuple["HTMLElement"]] = None,
        **attrs: Any,
    ):
        if not element_type:
            if not self.ELEMENT_TYPE:
                raise AttributeError(
                    "No value provided for required attribute `element_type`"
                )
            else:
                self.type = self.ELEMENT_TYPE
        else:
            self.type = element_type

        self.content = content or ""
        self.context = context or {}
        self.children = list(children) if children else []
        self.attrs: list[HTMLAttribute] = []
        if attrs:
            self.attrs = [HTMLAttribute(key, val) for key, val in attrs.items()]

    def serialize_attrs(self) -> str:
        if not self.attrs:
            return ""
        return " " + " ".join([attr.serialize() for attr in self.attrs])

    def serialize_children(self, pretty: bool, depth: int, indent: int) -> str:
        if not self.children:
            return ""
        serialized_children = ""
        for child in self.children:
            serialized_children += child.render(pretty, depth, indent)
        return serialized_children

    def render(self, pretty: bool = False, depth: int = 0, indent: int = 2) -> str:
        return (
            ("\n" if pretty and depth else "")
            + (" " * (depth * indent) if pretty else "")
            + f"<{self.type}{self.serialize_attrs()}>"
            + ("\n" + " " * (depth + 1) * indent if pretty and self.content else "")
            + f"{self.content}"
            + f"{self.serialize_children(pretty, depth+1, indent)}"
            + ("\n" + " " * (depth * indent) if pretty else "")
            + f"</{self.type}>"
        )

    def __call__(self, *children: "HTMLElement") -> Self:
        self.children.extend(list(children))
        return self

    def __str__(self) -> str:
        children_repr_list = []
        if self.children:
            for child in self.children:
                children_repr_list.append(str(child))
        children_repr = ", ".join(children_repr_list)
        return f"{self.type}({children_repr})"

    def __repr__(self) -> str:
        return self.__str__()


class div(HTMLElement):
    ELEMENT_TYPE = "div"


class span(HTMLElement):
    ELEMENT_TYPE = "span"


class strong(HTMLElement):
    ELEMENT_TYPE = "strong"


class section(HTMLElement):
    ELEMENT_TYPE = "section"
