import json
import os
import sys

files = sorted([ f for f in os.listdir(os.path.join(os.getcwd(),'contributors')) if '.json' in f ])
count = 0
for f in files:
    with open(os.path.join(os.getcwd(),'contributors/'+f)) as fh:
        jsonfile = json.loads(fh.read())
        if sorted(list(jsonfile.keys())) == ['about', 'batch', 'course', 'institution', 'name', 'skills_hobbies']:
            os.system(f"gh pr merge -m")
        else:
            sys.exit(f"'{'contributors/'+f}' is either missing one or more required keys, or contains inappropriate keys.")
