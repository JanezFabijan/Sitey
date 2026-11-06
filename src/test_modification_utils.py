
import unittest
from textnode import TextNode, TextType
from modification_utils import (
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
    markdown_to_blocks,
    block_to_block_type,
    BlockType,
    text_to_children,
    block_to_html_node,
    markdown_to_html_node,
    extract_title
)


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]

        self.assertEqual(new_nodes, expected)

    def test_bold(self):
        node = TextNode("This is **bold** text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)

        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]

        self.assertEqual(new_nodes, expected)

    def test_italic(self):
        node = TextNode("This is _italic_ text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)

        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT),
        ]

        self.assertEqual(new_nodes, expected)

    def test_multiple_delimiters(self):
        node = TextNode("This has **bold** and **more bold** text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)

        expected = [
            TextNode("This has ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("more bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]

        self.assertEqual(new_nodes, expected)

    def test_multiple_nodes(self):
        nodes = [
            TextNode("This is **bold** text", TextType.TEXT),
            TextNode("This is **also bold** text", TextType.TEXT),
        ]

        new_nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)

        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
            TextNode("This is ", TextType.TEXT),
            TextNode("also bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]

        self.assertEqual(new_nodes, expected)

    def test_non_text_node(self):
        node = TextNode("Already bold", TextType.BOLD)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)

        self.assertEqual(new_nodes, [node])

    def test_mixed_nodes(self):
        nodes = [
            TextNode("Already bold", TextType.BOLD),
            TextNode("This is `code` text", TextType.TEXT),
        ]

        new_nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)

        expected = [
            TextNode("Already bold", TextType.BOLD),
            TextNode("This is ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" text", TextType.TEXT),
        ]

        self.assertEqual(new_nodes, expected)

    def test_no_delimiter(self):
        node = TextNode("Just plain text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)

        self.assertEqual(new_nodes, [node])

    def test_unmatched_delimiter(self):
        node = TextNode("This is **invalid text", TextType.TEXT)

        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "**", TextType.BOLD)

    def test_empty_nodes(self):
        new_nodes = split_nodes_delimiter([], "**", TextType.BOLD)

        self.assertEqual(new_nodes, [])

    def test_sequential_splitting(self):
        node = TextNode("This is **bold** and _italic_ text", TextType.TEXT)

        nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)

        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT),
        ]

        self.assertEqual(nodes, expected)

    def test_empty_text_node(self):
        node = TextNode("", TextType.TEXT)

        expected = [node]

        self.assertEqual(
            split_nodes_delimiter([node], "**", TextType.BOLD),
            expected,
        )

    def test_delimiter_at_start(self):
        node = TextNode("**bold** text", TextType.TEXT)

        expected = [
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]

        self.assertEqual(
            split_nodes_delimiter([node], "**", TextType.BOLD),
            expected,
        )

    def test_delimiter_at_end(self):
        node = TextNode("Some **bold**", TextType.TEXT)

        expected = [
            TextNode("Some ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
        ]

        self.assertEqual(
            split_nodes_delimiter([node], "**", TextType.BOLD),
            expected,
        )

    def test_adjacent_delimiters(self):
        node = TextNode("**bold****more bold**", TextType.TEXT)

        expected = [
            TextNode("bold", TextType.BOLD),
            TextNode("more bold", TextType.BOLD),
        ]

        self.assertEqual(
            split_nodes_delimiter([node], "**", TextType.BOLD),
            expected,
        )

class TestSplitNodesImage(unittest.TestCase):
    def test_single_image(self):
        node = TextNode(
            "This is an ![image](https://example.com/image.png) example",
            TextType.TEXT,
        )

        expected = [
            TextNode("This is an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://example.com/image.png"),
            TextNode(" example", TextType.TEXT),
        ]

        self.assertEqual(split_nodes_image([node]), expected)

    def test_multiple_images(self):
        node = TextNode(
            "First ![cat](cat.png) and second ![dog](dog.png) done",
            TextType.TEXT,
        )

        expected = [
            TextNode("First ", TextType.TEXT),
            TextNode("cat", TextType.IMAGE, "cat.png"),
            TextNode(" and second ", TextType.TEXT),
            TextNode("dog", TextType.IMAGE, "dog.png"),
            TextNode(" done", TextType.TEXT),
        ]

        self.assertEqual(split_nodes_image([node]), expected)

    def test_image_at_start(self):
        node = TextNode("![cat](cat.png) after", TextType.TEXT)

        expected = [
            TextNode("cat", TextType.IMAGE, "cat.png"),
            TextNode(" after", TextType.TEXT),
        ]

        self.assertEqual(split_nodes_image([node]), expected)

    def test_image_at_end(self):
        node = TextNode("Before ![cat](cat.png)", TextType.TEXT)

        expected = [
            TextNode("Before ", TextType.TEXT),
            TextNode("cat", TextType.IMAGE, "cat.png"),
        ]

        self.assertEqual(split_nodes_image([node]), expected)

    def test_adjacent_images(self):
        node = TextNode("![cat](cat.png)![dog](dog.png)", TextType.TEXT)

        expected = [
            TextNode("cat", TextType.IMAGE, "cat.png"),
            TextNode("dog", TextType.IMAGE, "dog.png"),
        ]

        self.assertEqual(split_nodes_image([node]), expected)

    def test_no_images(self):
        node = TextNode("Just plain text", TextType.TEXT)

        self.assertEqual(split_nodes_image([node]), [node])

    def test_non_text_node(self):
        node = TextNode("Already bold", TextType.BOLD)

        self.assertEqual(split_nodes_image([node]), [node])

    def test_multiple_nodes(self):
        nodes = [
            TextNode("First ![cat](cat.png)", TextType.TEXT),
            TextNode("Second ![dog](dog.png)", TextType.TEXT),
        ]

        expected = [
            TextNode("First ", TextType.TEXT),
            TextNode("cat", TextType.IMAGE, "cat.png"),
            TextNode("Second ", TextType.TEXT),
            TextNode("dog", TextType.IMAGE, "dog.png"),
        ]

        self.assertEqual(split_nodes_image(nodes), expected)

    def test_empty_nodes(self):
        self.assertEqual(split_nodes_image([]), [])

    def test_empty_text_node(self):
        node = TextNode("", TextType.TEXT)

        self.assertEqual(split_nodes_image([node]), [node])

class TestSplitNodesLink(unittest.TestCase):
    def test_single_link(self):
        node = TextNode(
            "Visit [Google](https://google.com) today",
            TextType.TEXT,
        )

        expected = [
            TextNode("Visit ", TextType.TEXT),
            TextNode("Google", TextType.LINK, "https://google.com"),
            TextNode(" today", TextType.TEXT),
        ]

        self.assertEqual(split_nodes_link([node]), expected)

    def test_multiple_links(self):
        node = TextNode(
            "Visit [Google](https://google.com) and [GitHub](https://github.com)",
            TextType.TEXT,
        )

        expected = [
            TextNode("Visit ", TextType.TEXT),
            TextNode("Google", TextType.LINK, "https://google.com"),
            TextNode(" and ", TextType.TEXT),
            TextNode("GitHub", TextType.LINK, "https://github.com"),
        ]

        self.assertEqual(split_nodes_link([node]), expected)

    def test_link_at_start(self):
        node = TextNode("[Google](https://google.com) is useful", TextType.TEXT)

        expected = [
            TextNode("Google", TextType.LINK, "https://google.com"),
            TextNode(" is useful", TextType.TEXT),
        ]

        self.assertEqual(split_nodes_link([node]), expected)

    def test_link_at_end(self):
        node = TextNode("Visit [Google](https://google.com)", TextType.TEXT)

        expected = [
            TextNode("Visit ", TextType.TEXT),
            TextNode("Google", TextType.LINK, "https://google.com"),
        ]

        self.assertEqual(split_nodes_link([node]), expected)

    def test_adjacent_links(self):
        node = TextNode("[Google](google.com)[GitHub](github.com)", TextType.TEXT)

        expected = [
            TextNode("Google", TextType.LINK, "google.com"),
            TextNode("GitHub", TextType.LINK, "github.com"),
        ]

        self.assertEqual(split_nodes_link([node]), expected)

    def test_no_links(self):
        node = TextNode("Just plain text", TextType.TEXT)

        self.assertEqual(split_nodes_link([node]), [node])

    def test_non_text_node(self):
        node = TextNode("Already bold", TextType.BOLD)

        self.assertEqual(split_nodes_link([node]), [node])

    def test_multiple_nodes(self):
        nodes = [
            TextNode("Visit [Google](google.com)", TextType.TEXT),
            TextNode("And [GitHub](github.com)", TextType.TEXT),
        ]

        expected = [
            TextNode("Visit ", TextType.TEXT),
            TextNode("Google", TextType.LINK, "google.com"),
            TextNode("And ", TextType.TEXT),
            TextNode("GitHub", TextType.LINK, "github.com"),
        ]

        self.assertEqual(split_nodes_link(nodes), expected)

    def test_empty_nodes(self):
        self.assertEqual(split_nodes_link([]), [])

    def test_empty_text_node(self):
        node = TextNode("", TextType.TEXT)

        self.assertEqual(split_nodes_link([node]), [node])

class TestTextToTextNodes(unittest.TestCase):
    def test_plain_text(self):
        text = "Just plain text"

        expected = [
            TextNode("Just plain text", TextType.TEXT),
        ]

        self.assertEqual(text_to_textnodes(text), expected)

    def test_bold(self):
        text = "This is **bold** text"

        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]

        self.assertEqual(text_to_textnodes(text), expected)

    def test_italic(self):
        text = "This is _italic_ text"

        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT),
        ]

        self.assertEqual(text_to_textnodes(text), expected)

    def test_code(self):
        text = "This is `code` text"

        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" text", TextType.TEXT),
        ]

        self.assertEqual(text_to_textnodes(text), expected)

    def test_image(self):
        text = "An ![image](https://example.com/image.png) here"

        expected = [
            TextNode("An ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://example.com/image.png"),
            TextNode(" here", TextType.TEXT),
        ]

        self.assertEqual(text_to_textnodes(text), expected)

    def test_link(self):
        text = "Visit [Google](https://google.com) today"

        expected = [
            TextNode("Visit ", TextType.TEXT),
            TextNode("Google", TextType.LINK, "https://google.com"),
            TextNode(" today", TextType.TEXT),
        ]

        self.assertEqual(text_to_textnodes(text), expected)

    def test_all_types(self):
        text = (
            "This is **bold** with an _italic_ word "
            "and a `code block` and an "
            "![image](https://example.com/image.png) "
            "and a [link](https://example.com)"
        )

        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://example.com/image.png"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://example.com"),
        ]

        self.assertEqual(text_to_textnodes(text), expected)

    def test_multiple_bold_and_italic(self):
        text = "**first** and **second** plus _one_ and _two_"

        expected = [
            TextNode("first", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("second", TextType.BOLD),
            TextNode(" plus ", TextType.TEXT),
            TextNode("one", TextType.ITALIC),
            TextNode(" and ", TextType.TEXT),
            TextNode("two", TextType.ITALIC),
        ]

        self.assertEqual(text_to_textnodes(text), expected)

    def test_adjacent_formats(self):
        text = "**bold**_italic_`code`"

        expected = [
            TextNode("bold", TextType.BOLD),
            TextNode("italic", TextType.ITALIC),
            TextNode("code", TextType.CODE),
        ]

        self.assertEqual(text_to_textnodes(text), expected)

    def test_unmatched_delimiter(self):
        text = "This is **invalid"

        with self.assertRaises(ValueError):
            text_to_textnodes(text)

    def test_empty_text(self):
        expected = [TextNode("", TextType.TEXT)]

        self.assertEqual(text_to_textnodes(""), expected)

class TestMarkdownToBlocks(unittest.TestCase):
        def test_markdown_to_blocks(self):
            md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
            blocks = markdown_to_blocks(md)
            self.assertEqual(
                blocks,
                [
                    "This is **bolded** paragraph",
                    "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                    "- This is a list\n- with items",
                ],
            )

        def test_markdown_to_blocks_with_excessive_emptylines(self):
            md = """
This is **bolded** paragraph



This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line



- This is a list
- with items
"""
            blocks = markdown_to_blocks(md)
            self.assertEqual(
                blocks,
                [
                    "This is **bolded** paragraph",
                    "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                    "- This is a list\n- with items",
                ],
            )

        def test_markdown_to_blocks_with_whitespace_filled_lines(self):
            md = """
This is **bolded** paragraph

          
This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

            
      

- This is a list
- with items
"""
            blocks = markdown_to_blocks(md)
            self.assertEqual(
                blocks,
                [
                    "This is **bolded** paragraph",
                    "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                    "- This is a list\n- with items",
                ],
            )

        def test_markdown_to_blocks_with_emptyfile(self):
            md = """


      




"""
            blocks = markdown_to_blocks(md)
            self.assertEqual(
                blocks,
                [],
            )

class TestBlockToBlockType(unittest.TestCase):
    def test_paragraph(self):
        block = "This is a normal paragraph."
        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH,
        )

    def test_heading(self):
        for level in range(1, 7):
            block = f"{'#' * level} Heading"
            with self.subTest(level=level):
                self.assertEqual(
                    block_to_block_type(block),
                    BlockType.HEADING,
                )

    def test_invalid_heading(self):
        blocks = [
            "####### Too many hashes",
            "#Missing space",
            "##Missing space",
            "Normal # heading",
        ]

        for block in blocks:
            with self.subTest(block=block):
                self.assertEqual(
                    block_to_block_type(block),
                    BlockType.PARAGRAPH,
                )

    def test_code(self):
        block = "```\nprint('Hello World')\n```"
        self.assertEqual(
            block_to_block_type(block),
            BlockType.CODE,
        )

    def test_multiline_code(self):
        block = "```\nx = 1\ny = 2\nprint(x + y)\n```"
        self.assertEqual(
            block_to_block_type(block),
            BlockType.CODE,
        )

    def test_invalid_code(self):
        blocks = [
            "```python code```",
            "```\ncode without closing",
            "code\n```",
        ]

        for block in blocks:
            with self.subTest(block=block):
                self.assertEqual(
                    block_to_block_type(block),
                    BlockType.PARAGRAPH,
                )

    def test_quote(self):
        block = "> This is a quote"
        self.assertEqual(
            block_to_block_type(block),
            BlockType.QUOTE,
        )

    def test_multiline_quote(self):
        block = "> First line\n> Second line\n> Third line"
        self.assertEqual(
            block_to_block_type(block),
            BlockType.QUOTE,
        )

    def test_invalid_quote(self):
        block = "> First line\nSecond line"
        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH,
        )

    def test_unordered_list(self):
        block = "- First item\n- Second item\n- Third item"
        self.assertEqual(
            block_to_block_type(block),
            BlockType.UNORDERED_LIST,
        )

    def test_single_unordered_item(self):
        block = "- Single item"
        self.assertEqual(
            block_to_block_type(block),
            BlockType.UNORDERED_LIST,
        )

    def test_invalid_unordered_list(self):
        blocks = [
            "- First item\nSecond item",
            "-First item",
            "- First item\n* Second item",
        ]

        for block in blocks:
            with self.subTest(block=block):
                self.assertEqual(
                    block_to_block_type(block),
                    BlockType.PARAGRAPH,
                )

    def test_ordered_list(self):
        block = "1. First\n2. Second\n3. Third"
        self.assertEqual(
            block_to_block_type(block),
            BlockType.ORDERED_LIST,
        )

    def test_single_ordered_item(self):
        block = "1. First item"
        self.assertEqual(
            block_to_block_type(block),
            BlockType.ORDERED_LIST,
        )

    def test_invalid_ordered_list(self):
        blocks = [
            "1. First\n3. Third",
            "2. First\n3. Second",
            "1.First",
            "1. First\n2.Second",
            "1. First\n2. Second\n2. Duplicate",
        ]

        for block in blocks:
            with self.subTest(block=block):
                self.assertEqual(
                    block_to_block_type(block),
                    BlockType.PARAGRAPH,
                )

    def test_empty_block(self):
        self.assertEqual(
            block_to_block_type(""),
            BlockType.PARAGRAPH,
        )

class TestTextToChildren(unittest.TestCase):
    def test_bold_text(self):
        children = text_to_children("Hello **world**!")

        self.assertEqual(len(children), 3)
        self.assertEqual(children[0].to_html(), "Hello ")
        self.assertEqual(children[1].to_html(), "<b>world</b>")
        self.assertEqual(children[2].to_html(), "!")

class TestMarkdownToHTMLNode(unittest.TestCase):
    def test_paragraph(self):
        markdown = "This is a **bold** paragraph."

        html = markdown_to_html_node(markdown).to_html()

        self.assertEqual(
            html,
            "<div><p>This is a <b>bold</b> paragraph.</p></div>",
        )

    def test_heading(self):
        markdown = "## Hello **World**"

        html = markdown_to_html_node(markdown).to_html()

        self.assertEqual(
            html,
            "<div><h2>Hello <b>World</b></h2></div>",
        )

    def test_multiple_blocks(self):
        markdown = """# Hello World

This is a paragraph.

This is another **bold** paragraph."""

        html = markdown_to_html_node(markdown).to_html()

        expected = (
            "<div>"
            "<h1>Hello World</h1>"
            "<p>This is a paragraph.</p>"
            "<p>This is another <b>bold</b> paragraph.</p>"
            "</div>"
        )

        self.assertEqual(html, expected)

    def test_multiline_paragraph(self):
        markdown = """This is the first line
and this is the second line."""

        html = markdown_to_html_node(markdown).to_html()

        self.assertEqual(
            html,
            "<div><p>This is the first line and this is the second line.</p></div>",
        )

    def test_code_block(self):
        markdown = "```\nThis is **not bold**\n```"

        html = markdown_to_html_node(markdown).to_html()

        self.assertEqual(
            html,
            "<div><pre><code>This is **not bold**\n</code></pre></div>",
        )

    def test_quote(self):
        markdown = "> This is a **bold** quote"

        html = markdown_to_html_node(markdown).to_html()

        self.assertEqual(
            html,
            "<div><blockquote>This is a <b>bold</b> quote</blockquote></div>",
        )

    def test_unordered_list(self):
        markdown = """- First item
- Second **bold** item
- Third item"""

        html = markdown_to_html_node(markdown).to_html()

        expected = (
            "<div>"
            "<ul>"
            "<li>First item</li>"
            "<li>Second <b>bold</b> item</li>"
            "<li>Third item</li>"
            "</ul>"
            "</div>"
        )

        self.assertEqual(html, expected)


    def test_ordered_list(self):
        markdown = """1. First item
2. Second _italic_ item
3. Third item"""

        html = markdown_to_html_node(markdown).to_html()

        expected = (
            "<div>"
            "<ol>"
            "<li>First item</li>"
            "<li>Second <i>italic</i> item</li>"
            "<li>Third item</li>"
            "</ol>"
            "</div>"
        )

        self.assertEqual(html, expected)


    def test_mixed_blocks(self):
        markdown = """# My Document

This is a **paragraph**.

- First item
- Second item

1. Step one
2. Step two

> A quote

```
print("Hello")
```
"""

        html = markdown_to_html_node(markdown).to_html()

        expected = (
            "<div>"
            "<h1>My Document</h1>"
            "<p>This is a <b>paragraph</b>.</p>"
            "<ul><li>First item</li><li>Second item</li></ul>"
            "<ol><li>Step one</li><li>Step two</li></ol>"
            "<blockquote>A quote</blockquote>"
            '<pre><code>print("Hello")\n</code></pre>'
            "</div>"
        )

        self.assertEqual(html, expected)


class TestExtractTitle(unittest.TestCase):
    def test_simple_title(self):
        markdown = "# Hello World"
        self.assertEqual(extract_title(markdown), "Hello World")

    def test_title_with_whitespace(self):
        markdown = "#   Hello World   "
        self.assertEqual(extract_title(markdown), "Hello World")

    def test_title_after_paragraph(self):
        markdown = """Some text

# My Title

More text"""

        self.assertEqual(extract_title(markdown), "My Title")

    def test_multiple_headings(self):
        markdown = """## Subtitle

# Main Title

### Another heading"""

        self.assertEqual(extract_title(markdown), "Main Title")

    def test_no_title(self):
        markdown = "Just a paragraph without a heading"

        with self.assertRaises(ValueError):
            extract_title(markdown)

    def test_only_h2(self):
        markdown = "## Not an H1"

        with self.assertRaises(ValueError):
            extract_title(markdown)


if __name__ == "__main__":
    unittest.main()
