from textnode import TextNode, TextType

def main():
    # Create a TextNode instance
    text_node = TextNode("This is some anchor text", TextType.LINK, url="https://www.boot.dev")

    # Print the TextNode instance
    print(text_node)

if __name__ == "__main__":
    main()