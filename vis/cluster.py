#!/usr/bin/env python

import sys
from ovito.io import import_file
from ovito.modifiers import *

def crunch(inputFile):
    pipeline = import_file(inputFile)
    n_frames = pipeline.source.num_frames

    pipeline.modifiers.append(ExpressionSelectionModifier(
        expression='ParticleType!=3'))
    pipeline.modifiers.append(DeleteSelectedModifier())
    pipeline.modifiers.append(ClusterAnalysisModifier(
        cutoff=10,
        sort_by_size=True,
        compute_com=True))

    data_begin = pipeline.compute(0)
    ctab_begin = data_begin.tables['clusters']
    bub_ini = ctab_begin['Cluster Size'][...][0]
    pos_ini = ctab_begin['Center of Mass'][...][0]

    data_end = pipeline.compute(n_frames-1)
    ctab_end = data_end.tables['clusters']
    bub_fin = ctab_end['Cluster Size'][...][0]
    pos_fin = ctab_end['Center of Mass'][...][0]

    res = bub_ini - bub_fin
    print(res)

    dis2 = 0
    for i in range(3):
       dis2 += (pos_fin[i] - pos_ini[i])**2

    dis = dis2 ** 0.5
    print(dis)

    with open('cluster_data.txt', 'a') as f:
        f.write(f'{inputFile}\n' +
                f'Initial bubble occupancy: {bub_ini}\n' +
                f'Initial bubble position: {pos_ini}\n' +
                f'Final bubble occupancy: {bub_fin}\n' +
                f'Final bubble position: {pos_fin}\n' +
                f'Re-solved Xe atoms: {res}\n' +
                f'Bubble displacement: {dis} angstrom\n\n')

    with open('resolved_xe_num.txt', 'a') as f:
        f.write(f'{res}\n')

def main():
    files = sys.argv[1:]
    for file in files:
        crunch(file)

if __name__ == '__main__':
    main()
