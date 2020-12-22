import sys

current_satellite = ""
current_count = 0

for line in sys.stdin:
    line = line.rstrip()
    A = line.split('\t')
    if A[0] == current_satellite:
        current_count = current_count + 1
    else:
        if current_count > 0:
            out = '\t'.join([current_satellite, str(current_count)])
            sys.stdout.write(out + '\n')
        current_satellite = A[0]
        current_count = 1
if current_count > 0:
    out = '\t'.join([current_satellite, str(current_count)])
    sys.stdout.write(out + '\n')

