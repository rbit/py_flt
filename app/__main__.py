import sys
import time
import re

def main():
    MAX_TABLE_SIZE = 20
    CONSEC_INTRVL = 10
    SUPPR_TIMEOUT = 600
    SUPPR_NUM = 25
    LAST_SEEN_TIME_IDX = 0
    SUPPR_UNTIL_TIME_IDX = 1
    CONSEC_NUM_IDX = 2

    ptn = re.compile(r'^(\[\d+:\d+:\d+/)\d+\.\d+:')
    msgs = {}

    for line in sys.stdin:
        key = ptn.sub(r'\1', line)
        rec = msgs.get(key, (0, 0, 0))
        now = time.time()

        if rec[SUPPR_UNTIL_TIME_IDX] > now:
            continue

        rec = now, 0, (rec[CONSEC_NUM_IDX] + 1 if rec[LAST_SEEN_TIME_IDX] + CONSEC_INTRVL >= now else 0)

        if rec[CONSEC_NUM_IDX] < SUPPR_NUM:
            print(line, end='', flush=True)
        else:
            rec = rec[LAST_SEEN_TIME_IDX], now + SUPPR_TIMEOUT, rec[CONSEC_NUM_IDX]
            print('Suppressing message until ' +
                  str(time.strftime('%H:%M:%S', time.localtime(rec[SUPPR_UNTIL_TIME_IDX]))) +
                  ': ' +
                  line,
                  end='',
                  flush=True)

        msgs.pop(key, None)
        msgs[key] = rec

        if len(msgs) > MAX_TABLE_SIZE:
            del msgs[next(iter(msgs))]

    print(msgs)

if __name__ == "__main__":
    main()