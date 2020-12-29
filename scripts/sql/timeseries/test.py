import sys
sys.path.append("hittestservice_deps.zip")
from vault.hittest import HitTest
from datetime import datetime

dt = datetime(2017, 1, 1)
ht = HitTest(dt, "/share/nas2/data/vault/TLE_daily/")

sys.stdout.write(ht.invoke(dt, 45.0, -176.0) + '\n')
