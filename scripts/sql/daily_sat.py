import sys, io 

def load_minmax_ts():
    D = {}
    with open("tle_sat_day_minmax.tab") as f:
        for line in f:
            line = line.rstrip()
            F = line.split('\t')
            if len(F) == 3:
                D[F[0]] = {}
                D[F[0]]["min"] = int(F[1])
                D[F[0]]["max"] = int(F[2])
    return D
#
MINMAX_DICT = load_minmax_ts()

CURRENT_SAT = ""
DAY_DICT = {}

def init_DD(satellite):
    min_day = MINMAX_DICT[satellite]["min"]
    max_day = MINMAX_DICT[satellite]["max"]
    D = {}
    for d in range(min_day, max_day+1, 1):
        D[d] = []
    return D
#

def fill_empties(satellite):
    global DAY_DICT
    min_day = MINMAX_DICT[satellite]["min"]
    max_day = MINMAX_DICT[satellite]["max"]
    for day in range(min_day, max_day+1, 1):
        if len(DAY_DICT[day]) == 0:
            DAY_DICT[day] = DAY_DICT[day-1]  # should always have a starting record since min_day must exist
        DAY_DICT[day][1] = day               # <-- very important
#

def emit(satellite):
    global DAY_DICT
    if len(DAY_DICT) > 0:
        fill_empties(satellite)
        for d in DAY_DICT:
            output = '\t'.join(map(str, DAY_DICT[d]))
            sys.stdout.write(output + '\n')
#

for line in sys.stdin:
    line = line.rstrip()
    Fields = line.split('\t')
    if len(Fields) > 2:
        (satellite, day_str) = Fields[0:2]  # First 2 columns must be satellite and days since 2000.
        day = int(day_str)
        if satellite != CURRENT_SAT:
            emit(CURRENT_SAT)
            CURRENT_SAT = satellite
            DAY_DICT = init_DD(satellite)
        if len(DAY_DICT[day]) == 0 or DAY_DICT[day][1] != day:
            DAY_DICT[day] = Fields.copy()
        if day+1 in DAY_DICT:
            DAY_DICT[day+1] = Fields.copy()
#
emit(CURRENT_SAT)


