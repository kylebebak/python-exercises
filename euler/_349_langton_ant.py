"""
Client of LangtonSimulate, which uses the Ant and Grid data types.
Finds the number of black squares on the grid after the ant has
taken n steps.
"""

import sys, time

from lib import langton

start_time = time.time()
ls = langton.LangtonSimulate()
try:
    N = int(sys.argv[1])
except IndexError:
    print("The number of steps must be passed to this script.")
    sys.exit()
except ValueError:
    print("The number of steps must be an integer.")
    sys.exit()

print(
    '{0} black squares after {1} moves'.format(ls.num_black(N), N)
)
print('Duration: {0}s'.format(time.time() - start_time))
