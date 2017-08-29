import glob, os
import re
import requests

os.chdir("_posts")
name_regex = "[^]]+"
url_regex = "http[s]?://[^)]+"
markup_regex = '\[({0})]\(\s*({1})\s*\)'.format(name_regex, url_regex)


for file in glob.glob("*.md"):
    f = open(('../working/'+file), 'w')
    for i, line in enumerate(open(file)):
        for match in re.finditer(markup_regex, line):
            source, url  = match.groups()
            if "img" in source:
                filename = url[url.rfind("/")+1:]
                targetName = ("/images/" + filename)
                print line
                line = line.replace(url,targetName)
                print line
        f.write(line)  # python will convert \n to os.linesep
    f.close()
