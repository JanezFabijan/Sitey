import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(tag="p", value="This is some test text", children=None, props={"class": "width: 50px"})
        html_props = node.props_to_html()
        test_props = ' class="width: 50px"'
        self.assertEqual(html_props, test_props)

    def test_node_children(self):
        node = HTMLNode(
            tag="p",
            value="First child",
        )
        node2 = HTMLNode(
            tag="p",
            value="Second child",
        )
        node3 = HTMLNode(
            tag="p",
            children=[node, node2],
        )

        self.assertIsNotNone(node3.children)
        self.assertEqual(node3.children, [node, node2])

    def test_eq_value(self):
        node = HTMLNode(tag="p", value="This is some test text", children=None, props={"class": "width: 50px"})
        node2 = HTMLNode(tag="p", value="This is some test text", children=None, props={"class": "width: 50px"})

        self.assertEqual(node.value, node2.value)

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")

        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_p_with_props(self):
        node = LeafNode("p", "Hello, world!", {"class": "width: 50px"})

        self.assertEqual(node.to_html(), '<p class="width: 50px">Hello, world!</p>')

    def test_leaf_to_html_eq(self):
        node = LeafNode("p", "Hello, world!", {"class": "width: 50px"})
        node2 = LeafNode("p", "Hello, world!", {"class": "width: 50px"})

        self.assertEqual(node.to_html(), node2.to_html())

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")


    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
    )
