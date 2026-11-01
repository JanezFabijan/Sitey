from __future__ import annotations
from enum import Enum

class HTMLTag(Enum):
    PARAGRAPH = "p"
    HEADER1 = "h1"
    LINK = "a"
    IMAGE = 'img' 


class HTMLNode:
    def __init__(self, tag: HTMLTag | None = None, value: str | None = None, children: list[HTMLNode] | None = None, props: dict[str, str] | None = None):
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

        attributes = ''
        
        for key in self.props:
            attributes += f'{key}="{self.props[key]}"'

        return attributes