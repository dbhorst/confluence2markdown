# Confluence to markdown

A python script to convert html export from confluence to markdown.

### Install

Install uv https://docs.astral.sh/uv/getting-started/installation/, clone this repository and run for instructions:

```
uv run convert.py -h
```

### Usage

```
convert.py [-h] source dest

positional arguments
  source      source folder, i.e. path to Confluence html files to be converted to .md
  dest        destination folder, i.e. path to folder where to write converted .md-files, e.g. /tmp/conf-md
```

#### Export from confluence

Open the space you want to export. Open ```Space Tools```, tab ```Content Tools``` and open the tab ```Export```. Do a ```HTML``` export of the content you need. Unzip the export in a directory and run the python script.

```
uv run convert.py <source dir> <destination dir>
```

The destination dir will be deleted and recreated!
