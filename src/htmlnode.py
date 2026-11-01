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
        raise Exception(NotImplementedError)

    def props_to_html(self) -> str:
        if not self.props:
            return ''

        attributes = ' '
        
        for key in self.props:
            attributes += f'{key}="{self.props[key]}"'

        return attributes

class LeafNode(HTMLNode):
    def __init__(self, tag: str, value: str, props: dict[str, str] | None = None):
        super().__init__(tag, value, None, props)

    def __repr__(self):
        print(f"tag: {self.tag}")
        print(f"value: {self.value}")
        print(f"props: {self.props}")

    def to_html(self) -> str:
        if not self.value:
            raise Exception(ValueError)

        if not self.tag:
            return self.value

        return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'
