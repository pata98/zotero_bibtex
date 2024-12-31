# Zotero BibTeX Updater

This is a script to update a BibTeX file using the metadata from the PDFs in a Zotero WebDAV database folder.

## How to use
1. Install the dependencies
```bash
pip install -r requirements.txt
```

2. Run the script
```bash
python bibtex_updater.py --webdav-url http://your.url/dir --username user_name --password password
```

3. The script will update the BibTeX file with the metadata from the PDFs in the WebDAV database folder.


## Updates
- 2024.12.31: Initial release
- Automatic update version is coming soon...!