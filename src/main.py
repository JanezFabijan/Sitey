
from pathlib import Path
import shutil


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


def main():
    copy_static()

if __name__ == "__main__":
    main()
