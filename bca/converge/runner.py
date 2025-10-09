# create a new dir and copy input.toml
# run rustbca on it
# run surf_grid on output
# if not converged, redo the steps
#
# have a file with grid data - main file
# it'll have number of ions, avg. energy and avg. angle
# no list; just 3 gridwise values
#
# after every 1000 runs, we operate on the main and local files
# ion numbers are simply added
# grid elem list of energies are summed
# and added to N x avg. energy in the main file
# a new average is then created
# same for the avg. angle
# the main file is subsequently updated
#
# if 6 local grid elements have updated e, a, p by less than 1%
# consider everything converged

import os
import shutil
import subprocess

def get_next_run_dir(prefix='run_'):
    i = 1
    while os.path.exists(f'{prefix}{i}'):
        i += 1

    return f'{prefix}{i}'

def main():
    run_dir = get_next_run_dir()
    os.makedirs(run_dir)

    src_file = 'umo_0D.toml'
    dst_file = os.path.join(run_dir, src_file)
    shutil.copy(src_file, dst_file)

    subprocess.run(['../../RustBCA', '0D', src_file], cwd=run_dir)
    subprocess.run(['python', '../scripts/surf_grid.py',
                    f'{dst_file.split('.')[0]}'])

if __name__ == '__main__':
    main()
