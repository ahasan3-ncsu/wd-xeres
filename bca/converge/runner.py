import os
import sys
import shutil
import subprocess

def get_next_run_dir(prefix='run_'):
    i = 1
    while os.path.exists(f'{prefix}{i}'):
        i += 1

    return f'{prefix}{i}'

def do_sim():
    run_dir = get_next_run_dir()
    os.makedirs(run_dir)

    src_file = 'umo_0D.toml'
    dst_file = os.path.join(run_dir, src_file)
    shutil.copy(src_file, dst_file)

    subprocess.run(['../../RustBCA', '0D', src_file], cwd=run_dir)
    subprocess.run(['python', '../scripts/surf_grid.py',
                    f'{dst_file.split('.')[0]}'])

    return run_dir

def main():
    num_sims = int(sys.argv[1])

    for _ in range(num_sims):
        sim_dir = do_sim()
        print(f'{sim_dir} complete\n')

if __name__ == '__main__':
    main()
