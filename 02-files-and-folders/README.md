# Files and Folders

Part 2 builds a command-line file-maintenance assistant with Python's
standard library.

The tool can:

- Recursively scan a directory.
- Generate a CSV inventory report.
- List files larger than a selected size.
- Preview safe batch renaming.
- Rename top-level files only when `--execute` is supplied.

## Run

From this directory, scan a folder and create the default `inventory.csv`
report:

```powershell
python main.py "C:\path\to\folder"
```

Set a file-size threshold in megabytes:

```powershell
python main.py "C:\path\to\folder" --large 200
```

Preview batch renaming:

```powershell
python main.py "C:\path\to\folder" --rename --prefix Ghana_Project
```

Apply the preview:

```powershell
python main.py "C:\path\to\folder" --rename --prefix Ghana_Project --execute
```

The inventory and large-file scan include subdirectories, while batch
renaming only considers files directly inside the selected folder. The report
must be saved outside the scanned directory.
