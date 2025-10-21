import os
import sys
import glob
import shutil
import subprocess

def get_next_run_dir(dirpath):
    simpath = dirpath + '/run_'

    i = 1
    while os.path.exists(f'{simpath}{i}'):
        i += 1

    return f'{simpath}{i}'

def do_sim(dirpath):
    run_dir = get_next_run_dir(dirpath)
    os.makedirs(run_dir)

    input_file = '_'.join(['ballbox'] + dirpath.split('/')[:3]) + '.toml'

    src_file = os.path.join(dirpath, input_file)
    dst_file = os.path.join(run_dir, input_file)
    shutil.copy(src_file, dst_file)

    subprocess.run(['../../../../../RustBCA', 'SPHEREINCUBOID', input_file],
                   cwd=run_dir)
    res = subprocess.run(['python', '../scripts/xe_res.py', f'{dst_file[:-5]}'],
                         capture_output=True, text=True)

    with open(os.path.join(run_dir, 'xe_res.output'), 'w') as f:
        f.write(res.stdout)

    # do cleanup here
    for file in glob.glob(os.path.join(run_dir, 'ballbox_*.output')):
        os.remove(file)

    return run_dir

def main():
    dirpath = sys.argv[1]
    num_sims = int(sys.argv[2])

    for _ in range(num_sims):
        sim_dir = do_sim(dirpath)
        print(f'{sim_dir} complete\n')

if __name__ == '__main__':
    main()
