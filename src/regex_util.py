import re
from constants import markdown_image_regex, markdown_link_regex

def extract_markdown_images(text: str) -> list[tuple]:
    extracted_images: list[tuple] = []

    matches = re.findall(markdown_image_regex, text)

    for match in matches:
        extracted_images.append(match)

    return extracted_images

def extract_markdown_links(text: str) -> list[tuple]:
    extracted_links: list[tuple] = []

    matches = re.findall(markdown_link_regex, text)

    for match in matches:
        extracted_links.append(match)

    return extracted_links