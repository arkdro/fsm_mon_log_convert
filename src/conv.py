import re
import argparse

def extract_data(regex, match):
    date = match.group(1)
    time = match.group(2)
    max3 = match.group(3)
    items = max3.split(sep='}')
    vals = [extract_one_max(regex, x) for x in items if len(x) > 0]
    return (date, time, vals)

def extract_one_max(regex, x):
    res = re.search(regex, x)
    if res:
        return res.group(1)
    else:
        return -1

def proc_file(file):
    regex = re.compile('fsm_queue_mon.*datetime: (\d+-\d+-\d+)\D(\d+:\d+:\d+).*max3,\[([^\[\]]+)\]')
    max3_regex = re.compile('{(\d+)')
    with open(file, encoding='utf-8') as fd:
        for l in fd:
            match = re.search(regex, l)
            if match:
                data = extract_data(max3_regex, match)
                flush_item(data)

def flush_item(data):
    (date, time, vals) = data
    write_item(date, time, vals)

def write_item(date, time, vals):
    vals_str = ' '.join(map(str, vals))
    print(date, time, vals_str)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', "--input", help="input file")
    args = parser.parse_args()
    proc_file(args.input)

