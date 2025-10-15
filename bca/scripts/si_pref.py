def num_to_si(n):
    for unit in ['', 'k', 'M', 'G']:
        if n < 1e3:
            return f'{n:.0f}{unit}'
        n /= 1e3

    return f'{n:.0f}T'
