from pathlib import Path
import shutil


# Folder containing the files to organize.
SOURCE_DIR = Path("sample_files")

# Start in preview mode for safety.
DRY_RUN = True

# Map file extensions to destination folders.
FILE_CATEGORIES = {
	".pdf": "PDFs",
	".jpg": "Images",
	".jpeg": "Images",
	".png": "Images",
	".gif": "Images",
	".doc": "Documents",
	".docx": "Documents",
	".txt": "Text_Files",
	".csv": "Spreadsheets",
	".xls": "Spreadsheets",
	".xlsx": "Spreadsheets",
	".zip": "Archives",
	".rar": "Archives",
}


def get_destination(file_path):
	"""Determine the destination folder for a file."""

	category = FILE_CATEGORIES.get(file_path.suffix.lower(), "Others")
	return SOURCE_DIR / category


def unique_destination(destination):
	"""Avoid overwriting files with the same name."""

	if not destination.exists():
		return destination

	counter = 1

	while True:
		new_destination = (
			destination.parent
			/ f"{destination.stem}_{counter}{destination.suffix}"
		)

		if not new_destination.exists():
			return new_destination

		counter += 1


def organize_files():
	"""Organize files according to their extensions."""

	if not SOURCE_DIR.is_dir():
		print(f"Folder not found: {SOURCE_DIR}")
		return

	files = [item for item in SOURCE_DIR.iterdir() if item.is_file()]

	if not files:
		print("No files found to organize.")
		return

	for file_path in files:
		destination_folder = get_destination(file_path)
		destination = unique_destination(destination_folder / file_path.name)

		if DRY_RUN:
			print(
				f"[PREVIEW] {file_path.name} "
				f"-> {destination_folder.name}/{destination.name}"
			)
		else:
			destination_folder.mkdir(parents=True, exist_ok=True)
			shutil.move(str(file_path), str(destination))
			print(f"Moved: {file_path.name}")

	if DRY_RUN:
		print("\nPreview completed.")
		print("Set DRY_RUN = False to move the files.")


if __name__ == "__main__":
	organize_files()
