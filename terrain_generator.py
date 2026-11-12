import numpy as np
import random
import math

class Terrain_Generator:
    def __init__(self, seed):
        self._seed = seed
        self._permutations = np.zeros(255)
        self._gradients = np.array(list(zip(np.zeros(255), np.zeros(255))))
        print(self._permutations)
        print(self._gradients)
        random.seed(seed)
        for p in self._permutations:
            p = random.randint(0,255)
        for g in self._gradients:
            g[0], g[1] = random.randint(-127, 127), random.randint(-127, 127)
            length = math.sqrt(g[0]**2 + g[1] ** 2)
            g[0], g[1] = g[0] / length, g[1] / length
        print(self._permutations)
        print(self._gradients)
    def random_vector_2d_fast(self,x,y) - tuple[int,int]:
        i = self._permutations[x & 255]
        j = self._permutations[(y+i) & 255]
        return tuple(self._gradients[int(j)])
    def calc_coord(self, coordinate: tuple[int,int]):
        ws = {} # values to weight
        # sample vector is coordinate
        x = coordinate[0]
        y = coordinate[1]
        x1 = math.floor(x) - 1
        x2 = math.ceil(x) + 1
        y1 = math.floor(y) - 1
        y2 = math.ceil(y) + 1
        for h in [(x1,y1), (x1, y2), (x2, y1), (x1, y2)]:
            g = self.random_vector_2d_fast(h[0], h[1])
            v = (x - g[0], y - g[1])
            ws[h] = g[0] * v[0], g[1], v[1]
    def generate_chunk(self, chunk_coordinates: tuple[int, int]): # chunks are 16x16 units
        cc = chunk_coordinates
        x1 = cc[0] * 16
        y1 = cc[1] * 16
        x2 = cc[0] * 16 + 16
        y2 = cc[1] * 16 + 16
        for coord

if __name__ == "__main__":
    tgen = Terrain_Generator(1337)