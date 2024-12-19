import argparse
import shutil
import os

from markitdown import MarkItDown

# global vars
title = "none"

# Confluence sometimes has cryptic filenames, just consisting of digits. In that case, 
# the parsed title is used instead of the original filename. If filename already has 
# a string name, it is just returned.
def getMarkdownFilename(filename):
    if filename.isdigit():
        titleFilename = title
        position_colon = titleFilename.find(" : ")
        if position_colon >= 0 :
            titleFilename = titleFilename[(position_colon+3):]
        titleFilename = titleFilename.replace(" ", "-")
        titleFilename = titleFilename.replace("++", "pp")
        titleFilename = titleFilename.replace("/", "")
        titleFilename = titleFilename.replace("+", "")
        titleFilename = titleFilename.replace("_", "-")
        titleFilename = titleFilename.replace("---", "-")
        titleFilename = titleFilename.replace("--", "-")
        titleFilename = titleFilename.replace(".", "-")
        titleFilename = titleFilename.replace(":", "")
        titleFilename = titleFilename.replace("*", "")
        titleFilename = titleFilename.replace("<", "-")
        titleFilename = titleFilename.replace(">", "-")
        titleFilename = titleFilename.replace(",", "")
        titleFilename = titleFilename.replace(";", "")
        titleFilename = titleFilename.replace("?", "")
        titleFilename = titleFilename.replace("\"", "")
        titleFilename = titleFilename.replace("'", "")
       
        print("Renaming:", filename, " -> ", title, " -> ", titleFilename)
        return titleFilename
    else:
        return filename


# setup program arguments:
parser = argparse.ArgumentParser()
parser.add_argument("source", help="source folder, i.e. path to Confluence html files to be converted to .md")
parser.add_argument("dest", help="destination folder, i.e. path to folder where to write converted .md-files, e.g. /tmp/conf-md")
args = parser.parse_args()

# print info
print( "------------------------------" )
print( "Converting Confluence (.html to .md) from" )
print( args.source )
print( "to" )
print( args.dest )
print( "------------------------------" )

# copy whole source tree to destination, i.e. the .html files.
# This makes it easier to handle path+folder and new .md files.
# Plus, if conversion fails for some files, one can inspect remaining html files.
if os.path.exists(args.dest):
    shutil.rmtree(args.dest)
shutil.copytree(args.source, args.dest)

markitdown = MarkItDown()
# iterate all files. Read in html, write out md
for root, dirs, files in os.walk(args.dest):
    for file in files:
        filename, extension = os.path.splitext(file)
        # print file, filename, extension
        # skip non-html files:
        if not extension == '.html':
            continue

        # read html
        html_file_path = os.path.join(root, file)

        # convert html to markdown
        result = markitdown.convert(html_file_path)
        markdown_content = result.text_content
        title = result.title

        # write markdown to .md file
        markdown_filename = "%s.md" % getMarkdownFilename(filename)
        markdown_file_path = os.path.join(root, markdown_filename)
        with open(markdown_file_path, 'w', encoding="utf-8") as fout:
            fout.write(markdown_content)

        # remove copied .html file
        os.remove(html_file_path)
