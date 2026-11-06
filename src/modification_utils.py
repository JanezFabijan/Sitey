from textnode import TextNode, TextType
from regex_util import extract_markdown_images, extract_markdown_links
from enum import Enum
import re
from htmlnode import ParentNode, HTMLNode
from textnode import text_node_to_html_node

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def split_nodes_delimiter(
    old_nodes: list[TextNode],
    delimiter: str,
    text_type: TextType,
) -> list[TextNode]:
    return_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            return_nodes.append(node)
            continue

        parts = node.text.split(delimiter)

        if len(parts) % 2 == 0:
            raise ValueError("Invalid Markdown syntax: unmatched delimiter")

        for i, part in enumerate(parts):
            if not node.text:
                return_nodes.append(node)
                continue

            if not part:
                continue

            if i % 2 == 0:
                return_nodes.append(TextNode(part, TextType.TEXT))
            else:
                return_nodes.append(TextNode(part, text_type))

    return return_nodes


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        images = extract_markdown_images(node.text)

        if not images:
            new_nodes.append(node)
            continue

        remaining_text = node.text

        for alt, url in images:
            markdown = f"![{alt}]({url})"
            before, _, remaining_text = remaining_text.partition(markdown)

            if before:
                new_nodes.append(TextNode(before, TextType.TEXT))

            new_nodes.append(TextNode(alt, TextType.IMAGE, url))

        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))

    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        links = extract_markdown_links(node.text)

        if not links:
            new_nodes.append(node)
            continue

        remaining_text = node.text

        for anchor, url in links:
            markdown = f"[{anchor}]({url})"
            before, _, remaining_text = remaining_text.partition(markdown)

            if before:
                new_nodes.append(TextNode(before, TextType.TEXT))

            new_nodes.append(TextNode(anchor, TextType.LINK, url))

        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))

    return new_nodes

def text_to_textnodes(text: str) -> list[TextNode]:
    nodes = [TextNode(text, TextType.TEXT)]

    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)

    return nodes

def markdown_to_blocks(markdown: str) -> list[str]:
    line_strings: list[str] = markdown.split('\n\n')
    return_line_strings: list[str] = []

    for line in line_strings:
        current_line = line.strip()

        if current_line == "" or current_line == "\n\n":
            continue

        return_line_strings.append(current_line)


    return return_line_strings

def block_to_block_type(block: str) -> BlockType:
    lines = block.split("\n")

    match block:
        case b if re.fullmatch(r"#{1,6} .+", b):
            return BlockType.HEADING

        case b if b.startswith("```\n") and b.endswith("```"):
            return BlockType.CODE

        case _ if all(line.startswith(">") for line in lines):
            return BlockType.QUOTE

        case _ if all(line.startswith("- ") for line in lines):
            return BlockType.UNORDERED_LIST

        case _ if all(
            line.startswith(f"{i}. ")
            for i, line in enumerate(lines, start=1)
        ):
            return BlockType.ORDERED_LIST

        case _:
            return BlockType.PARAGRAPH

def text_to_children(text: str) -> list[HTMLNode]:
    text_nodes = text_to_textnodes(text)
    children = []

    for node in text_nodes:
        html_node = text_node_to_html_node(node)
        children.append(html_node)

    return children

def block_to_html_node(block: str) -> HTMLNode:
    block_type = block_to_block_type(block)

    match block_type:
        case BlockType.PARAGRAPH:
            text = " ".join(block.split("\n"))
            return ParentNode("p", text_to_children(text))

        case BlockType.HEADING:
            level = len(block) - len(block.lstrip("#"))
            text = block[level + 1:]
            return ParentNode(f"h{level}", text_to_children(text))

        case BlockType.CODE:
            text = block[4:-3]
            return ParentNode("pre", [
                text_node_to_html_node(TextNode(text, TextType.CODE))
            ])

        case BlockType.QUOTE:
            lines = block.split("\n")
            text = "\n".join(line.lstrip(">").strip() for line in lines)
            return ParentNode("blockquote", text_to_children(text))

        case BlockType.UNORDERED_LIST:
            items: list[HTMLNode] = []

            for line in block.split("\n"):
                text = line[2:]
                items.append(ParentNode("li", text_to_children(text)))

            return ParentNode("ul", items)

        case BlockType.ORDERED_LIST:
            items: list[HTMLNode] = []

            for line in block.split("\n"):
                text = line.split(". ", 1)[1]
                items.append(ParentNode("li", text_to_children(text)))

            return ParentNode("ol", items)

        case _:
            raise ValueError(f"Unsupported block type: {block_type}")

def markdown_to_html_node(markdown: str) -> ParentNode:
    children: list[HTMLNode] = []

    blocks = markdown_to_blocks(markdown)

    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)

    return ParentNode("div", children)

        


    return return_node