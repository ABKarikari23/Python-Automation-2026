from __future__ import annotations

import argparse
import csv
from pathlib import Path


def scan_directory(folder: Path) -> list[Path]:
    """Return all files inside a directory recursively."""
    return sorted(path for path in folder.rglob("*") if path.is_file())


def generate_inventory(files: list[Path], output_file: Path) -> None:
    """Create a CSV report containing each file's name, type, size, and path."""
    with output_file.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["File Name", "Extension", "Size (MB)", "Full Path"])

        for file in files:
            size_mb = file.stat().st_size / (1024 * 1024)
            writer.writerow(
                [file.name, file.suffix, round(size_mb, 2), str(file)]
            )

    print(f"Inventory report saved: {output_file}")


def find_large_files(files: list[Path], minimum_mb: float) -> None:
    """Display files larger than the specified size."""
    print(f"\nFiles larger than {minimum_mb:g} MB:")
    found = False

    for file in files:
        size_mb = file.stat().st_size / (1024 * 1024)
        if size_mb > minimum_mb:
            print(f"{file.name}: {size_mb:.2f} MB")
            found = True

    if not found:
        print("No matching files found.")


def batch_rename(
    files: list[Path], prefix: str, execute: bool = False
) -> None:
    """Preview or perform safe batch renaming for files in one directory."""
    if not files:
        print("\nNo files available for renaming.")
        return

    candidates = [file for file in files if file.parent == files[0].parent]
    reserved_names = {file.name.casefold() for file in candidates}
    planned: list[tuple[Path, Path]] = []

    for number, file in enumerate(candidates, start=1):
        base_name = f"{prefix}_{number:03d}"
        new_name = f"{base_name}{file.suffix.lower()}"
        counter = 1

        while new_name.casefold() in reserved_names:
            new_name = f"{base_name}_{counter}{file.suffix.lower()}"
            counter += 1

        reserved_names.add(new_name.casefold())
        planned.append((file, file.with_name(new_name)))

    for source, destination in planned:
        print(f"{source.name} -> {destination.name}")
        if execute:
            source.rename(destination)

    if not execute:
        print("\nPreview only. No files were renamed.")
        print("Run again with --execute to apply changes.")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Python File Maintenance Assistant"
    )
    parser.add_argument("folder", help="Directory to scan")
    parser.add_argument(
        "--report",
        default="inventory.csv",
        help="CSV inventory report filename",
    )
    parser.add_argument(
        "--large",
        type=float,
        default=100,
        help="Minimum file size in MB",
    )
    parser.add_argument(
        "--rename",
        action="store_true",
        help="Preview or perform batch renaming",
    )
    parser.add_argument(
        "--prefix",
        default="Project",
        help="Prefix for renamed files",
    )
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Actually perform batch renaming",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    folder = Path(args.folder).expanduser().resolve()

    if not folder.is_dir():
        raise SystemExit("The specified directory does not exist.")
    if args.large < 0:
        raise SystemExit("--large must be zero or greater.")
    if args.execute and not args.rename:
        raise SystemExit("--execute requires --rename.")

    report_path = Path(args.report).expanduser().resolve()
    if report_path == folder or folder in report_path.parents:
        raise SystemExit(
            "Save the inventory report outside the scanned directory."
        )

    files = scan_directory(folder)
    print(f"\nFiles found: {len(files)}")
    generate_inventory(files, report_path)
    find_large_files(files, args.large)

    if args.rename:
        top_level_files = sorted(
            file for file in folder.iterdir() if file.is_file()
        )
        batch_rename(top_level_files, args.prefix, execute=args.execute)


if __name__ == "__main__":
    main()
