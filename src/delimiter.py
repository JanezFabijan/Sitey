from textnode import TextNode, TextType

def split_nodes_delimiter(
    old_nodes: list[TextNode],
    delimiter: str,
    text_type: TextType
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
            if i % 2 == 0:
                return_nodes.append(TextNode(part, TextType.TEXT))
            else:
                return_nodes.append(TextNode(part, text_type))

    return return_nodes