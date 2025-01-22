# Zotero BibTeX Updater

This is a script to update a BibTeX file using the metadata from the PDFs in a Zotero WebDAV database folder.

## How to use
### Installing
#### pip
```bash
pip install -r requirements.txt
```
#### docker
```bash
docker build -t zotero-bibtex -f Dockerfile.zoterobibtex .
```
```bash
docker run -it --name 'zotero_bib' -v dir/of/bibtex zotero-bibtex
```

### Running the script
```bash
python3 bibtex_updater.py --webdav-url http://your.url/dir:port/zotero --username user_name --password password --bibtex-path path_of_bibtex.bib
```

## Updates
- 2024.12.31: Initial release
- 2025.01.22: Update dockerfile

## To Do
- [ ] Automatic syncing
- [ ] Fix metadata read bug
