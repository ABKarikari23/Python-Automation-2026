# Introduction to Python Automation

Part 1 introduces Python automation through a practical file organizer.

## Project

The `file-organizer` project scans files in `sample_files/` and groups them into folders based on their file extensions.

```text
file-organizer/
├── organizer.py
└── sample_files/
    ├── backup.zip
    ├── budget.xlsx
    ├── notes.txt
    ├── photograph.jpg
    ├── presentation.docx
    └── report.pdf
```

## Run the Organizer

Open a terminal in the `file-organizer` directory and run:

```powershell
python organizer.py
```

The script starts with `DRY_RUN = True`, so it previews the planned changes without moving files. After reviewing the preview, set `DRY_RUN = False` in `organizer.py` and run the script again to organize the files.

## Concepts Covered

- Rule-based automation
- File and folder paths with `pathlib`
- Moving files with `shutil`
- File-extension categorization
- Preview mode for safer execution
- Duplicate filename protection
- The automation workflow: input, processing, decision, action, and result

Unknown file extensions are placed in an `Others` folder, and duplicate names receive a numbered suffix such as `report_1.pdf`.
