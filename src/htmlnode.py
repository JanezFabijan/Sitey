from __future__ import annotations

class HTMLNode:
    def __init__(self, tag: str | None = None, value: str | None = None, children: list[HTMLNode] | None = None, props: dict[str, str] | None = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __repr__(self):
        print(f"tag: {self.tag}")
        print(f"value: {self.value}")
        print(f"children: {self.children}")
        print(f"props: {self.props}")

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self) -> str:
        if self.props is None:
            return ""

        attributes = ""

        for key in self.props:
            attributes += f' {key}="{self.props[key]}"'

        return attributes

class LeafNode(HTMLNode):
    def __init__(self, tag: str | None, value: str, props: dict[str, str] | None = None):
        super().__init__(tag, value, None, props)

    def __repr__(self):
        print(f"tag: {self.tag}")
        print(f"value: {self.value}")
        print(f"props: {self.props}")

    def to_html(self) -> str:
        if self.value is None:
            raise ValueError("LeafNode must have a value")

        if self.tag is None:
            return self.value

        return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'

class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: list[HTMLNode], props: dict[str, str] | None = None):
        super().__init__(tag, None, children, props)

    def to_html(self):

        if not self.tag:
            raise ValueError()

        if not self.children:
            raise ValueError("Where are the children?")

        html_string = f'<{self.tag}{self.props_to_html()}>'

        for child in self.children:
            html_string = html_string + child.to_html()
        html_string = html_string + f"</{self.tag}>"

        return html_string
