import sys, io

YEAR=2017
MONTH=1

for day in range(1,31+1,1):
    fname = "%4d-%02d-%02d.tab"%(YEAR, MONTH, day)
    with open(fname, "w") as f:
        for hour in range(24):
            line = "%4d-%02d-%02d %02d:00:00\t45.0\t-176.0"%(YEAR, MONTH, day, hour)
            f.write(line + '\n')

