import unittest
from htmlnode import HTMLNode, HTMLTag

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(tag=HTMLTag.PARAGRAPH, value="This is some test text", children=None, props={"class": "width: 50px"})
        html_props = node.props_to_html()
        test_props = 'class="width: 50px"'
        self.assertEqual(html_props, test_props)

    def test_node_children(self):
        node = HTMLNode(
            tag=HTMLTag.PARAGRAPH,
            value="First child",
        )
        node2 = HTMLNode(
            tag=HTMLTag.PARAGRAPH,
            value="Second child",
        )
        node3 = HTMLNode(
            tag=HTMLTag.PARAGRAPH,
            children=[node, node2],
        )

        self.assertIsNotNone(node3.children)
        self.assertEqual(node3.children, [node, node2])

    def test_eq(self):
        node = HTMLNode(tag=HTMLTag.PARAGRAPH, value="This is some test text", children=None, props={"class": "width: 50px"})
        node2 = HTMLNode(tag=HTMLTag.PARAGRAPH, value="This is some test text", children=None, props={"class": "width: 50px"})


        self.assertNotEqual(node, node2)
        