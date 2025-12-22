import os
import sys
import copy
import json
from statistics import mean, stdev

def get_sim_dir(dirpath):
    simpath = dirpath + '/run_'

    i = 1
    while True:
        yield f'{simpath}{i}'
        i += 1

def process_output(out_file, data):
    with open(out_file, 'r') as f:
        tmp = f.readline()
        data['xe_recoils'] += int(tmp.split()[-1])

        tmp = f.readline()
        data['xe_outside'] += int(tmp.split()[-1])

        tmp = f.readline()
        res = int(tmp.split()[-1])
        data['re-solved'] += res
        data['ls_res'].append(res)

    return True

def diff_output(old_data, new_data):
    if not old_data['sim_runs']:
        return 42.0

    old_res_per_sim = old_data['re-solved'] / old_data['sim_runs']
    new_res_per_sim = new_data['re-solved'] / new_data['sim_runs']

    if old_res_per_sim:
        return abs(new_res_per_sim / old_res_per_sim - 1)
    else:
        return 43.0

def main():
    dirpath = sys.argv[1]
    dir_gen = get_sim_dir(dirpath)

    old_data = {
        'sim_runs': 0,
        'xe_recoils': 0,
        'xe_outside': 0,
        're-solved': 0,
        'ls_res': []
    }
    new_data = copy.deepcopy(old_data)

    diff = 41.0

    while diff > 1e-3:
    # for _ in range(5):
        output_file = 'xe_res.output'
        output_path = os.path.join(next(dir_gen), output_file)
        if not os.path.exists(output_path):
            break

        new_data['sim_runs'] += 1
        process_output(output_path, new_data)
        diff = diff_output(old_data, new_data)
        print('DIFF: ', diff)

        old_data = copy.deepcopy(new_data)

    new_data['mean'] = mean(new_data['ls_res'])
    new_data['stdev'] = stdev(new_data['ls_res'])
    del new_data['ls_res']

    with open(os.path.join(dirpath, 'xe_res.json'), 'w') as f:
        json.dump(new_data, f, indent=4)

if __name__ == '__main__':
    main()
