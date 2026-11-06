
from pathlib import Path
import shutil
from modification_utils import markdown_to_html_node, extract_title

def copy_directory(source: Path, destination: Path) -> None:
    destination.mkdir(parents=True, exist_ok=True)

    for item in source.iterdir():
        target = destination / item.name

        if item.is_dir():
            copy_directory(item, target)

        elif item.is_file():
            print(f"Copying {item} -> {target}")
            shutil.copy2(item, target)

def copy_static() -> None:
    root = Path(__file__).resolve().parent.parent
    source = root / "static"
    destination = root / "public"

    if not source.is_dir():
        raise FileNotFoundError(f"Missing static directory: {source}")

    if destination.exists():
        shutil.rmtree(destination)

    copy_directory(source, destination)


def generate_page(
    from_path: Path,
    template_path: Path,
    dest_path: Path,
) -> None:
    print(f"Generating page from {from_path} to {dest_path}")

    # 1. Read markdown content
    markdown = from_path.read_text(encoding="utf-8")

    # 2. Read HTML template
    template = template_path.read_text(encoding="utf-8")

    # 3. Extract title from markdown
    title = extract_title(markdown)

    # 4. Convert markdown to HTML
    html = markdown_to_html_node(markdown).to_html()

    # 5. Replace placeholders
    page = template.replace("{{ Title }}", title)
    page = page.replace("{{ Content }}", html)

    # 6. Create destination directory if needed
    dest_path.parent.mkdir(parents=True, exist_ok=True)

    # 7. Write generated HTML
    dest_path.write_text(page, encoding="utf-8")


def main():
    root = Path(__file__).resolve().parent.parent

    copy_static()

    generate_page(
        root / "content" / "index.md",
        root / "template.html",
        root / "public" / "index.html",
    )

if __name__ == "__main__":
    main()
