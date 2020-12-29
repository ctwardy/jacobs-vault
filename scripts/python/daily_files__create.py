import gzip
import io 
import sys
from pathlib import Path

DIR0 = "/share/nas2/data/vault/TLE_daily"

CURRENT = ""
CURRENT_ZIP = None

def change_target(date_str):
    global CURRENT
    global CURRENT_ZIP
    if CURRENT_ZIP != None:
        CURRENT_ZIP.close()
    dir1 = date_str[0:4]
    dir2 = date_str[5:7]
    file = date_str[8:10]
    new_path = DIR0 + "/" + dir1 + "/" + dir2
    Path(new_path).mkdir(parents=True, exist_ok=True)
    new_path = new_path + "/" + file + ".tab.gz"
    CURRENT_ZIP =  gzip.open(new_path, 'at')
    CURRENT = date_str
#

for line in sys.stdin:
    line = line.strip()
    Fields = line.split('\t')
    if len(Fields) > 0:
        date_str = Fields[0][0:10]
        if date_str != CURRENT:
            change_target(date_str)

        output = '\t'.join(Fields[1:])
        CURRENT_ZIP.write(output + '\n')
#
CURRENT_ZIP.close()

