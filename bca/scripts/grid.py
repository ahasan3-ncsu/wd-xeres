rows = 9
cols = 3

# init
grid = []
for i in range(rows):
    row = []
    for j in range(cols):
        point = {
            'surf_area': 0.0,
            'num_ions': 0,
            'energies': [],
            'angles': []
        }
        row.append(point)
    grid.append(row)

grid[2][2]['surf_area'] = 3.1

# output
for i in range(rows):
    for j in range(cols):
        print(f'[{i},{j}] -> {grid[i][j]['surf_area']}', end='; ')
    print()
