import os
import shutil

p_eq = {1: 0.00905, 2: 0.00908, 4: 0.01009, 8: 0.00868, 16: 0.00662, 32: 0.00479, 64: 0.00327, 128: 0.00209}

Y_en = [102, 80, 60, 40, 20, 10, 5, 2, 1, 0.5, 0.1]
I_en = [75, 60, 40, 20, 10, 5, 2, 1, 0.5, 0.1]

radii = [64, 128]

for rad in radii:
    os.makedirs(f'{rad}nm', exist_ok=True)
    for y_e in Y_en:
        os.makedirs(f'{rad}nm/Y_{y_e}MeV', exist_ok=True)
    for i_e in I_en:
        os.makedirs(f'{rad}nm/I_{i_e}MeV', exist_ok=True)
