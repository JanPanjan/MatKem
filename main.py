import numpy as np

#matrika
W = np.array([
    [14, 14, 6,  1],
    [14, 20, 15, 6],
    [6,  15, 20, 14],
    [1,  6,  14, 14],
])

print(np.linalg.det(W))