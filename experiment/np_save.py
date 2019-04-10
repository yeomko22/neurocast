import numpy as np

def save_np():
    a = np.random.randn(5, 5)
    np.save('test.npy', a)

def load_np():
    b = np.load('test.npy')
    print(b)

def test_binary():
    pass

if __name__ == '__main__':
    # save_np()
    load_np()
