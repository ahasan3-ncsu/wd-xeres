import numpy as np

def get_mean(num_ions, quantity):
    assert len(num_ions) == len(quantity)

    return np.sum(quantity) / np.sum(num_ions)

def get_std(num_ions, quantity):
    assert len(num_ions) == len(quantity)

    ni = np.array(num_ions)
    qt = np.array(quantity)

    rate = qt / ni
    ext_rate = np.repeat(rate, ni)

    return np.std(ext_rate, ddof=1)

def main():
    ion_counts = [10,5,10,7,10]
    ex_quant = [30,21,32,25,33]

    print(get_mean(ion_counts, ex_quant))
    print(get_std(ion_counts, ex_quant))

if __name__ == '__main__':
    main()
