from ternary.helpers import simplex_iterator


def GenerateCoords(reps, scale):
    param = []
    for (i, j, k) in simplex_iterator(scale):
        for _ in range(reps):
            param.append([i / scale, j / scale, k / scale])
    return param


reps = 10
scale = 50  # increment = 1/scale
param = GenerateCoords(reps, scale)
# print(param)
print(len(param))
