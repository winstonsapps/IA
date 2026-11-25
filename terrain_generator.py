import numpy as np
import random
import math

if __name__ == "__main__":
    large_width = 400
    np.set_printoptions(linewidth=large_width)

"""
Blocks:
1: grass
2: Dirt
3. Stone
4. Water
"""

class TerrainGenerator:
    """
    Terrain generator class
    Doesn't generate meshes but makes noise
    Use block_height to get the block height at a certain x, z coordinate, returns a float between (0-255)
    """
    def __init__(self, seed, world_gen_options: dict): #TODO: add world gen options
        self._seed = seed
        self._permutations = np.array(
            [
                151, 160, 137,  91,  90,  15, 131,  13, 201,  95,  96,  53, 194, 233,   7, 225,
                140,  36, 103,  30,  69, 142,   8,  99,  37, 240,  21,  10,  23, 190,   6, 148,
                247, 120, 234,  75,   0,  26, 197,  62,  94, 252, 219, 203, 117,  35,  11,  32,
                57,  177,  33,  88, 237, 149,  56,  87, 174,  20, 125, 136, 171, 168,  68, 175,
                74,  165,  71, 134, 139,  48,  27, 166,  77, 146, 158, 231,  83, 111, 229, 122,
                60,  211, 133, 230, 220, 105,  92,  41,  55,  46, 245,  40, 244, 102, 143,  54,
                65,   25,  63, 161,   1, 216,  80,  73, 209,  76, 132, 187, 208,  89,  18, 169,
                200, 196, 135, 130, 116, 188, 159,  86, 164, 100, 109, 198, 173, 186,   3,  64,
                52,  217, 226, 250, 124, 123,   5, 202,  38, 147, 118, 126, 255,  82,  85, 212,
                207, 206,  59, 227,  47,  16,  58,  17, 182, 189,  28,  42, 223, 183, 170, 213,
                119, 248, 152,   2,  44, 154, 163,  70, 221, 153, 101, 155, 167,  43, 172,   9,
                129,  22,  39, 253,  19,  98, 108, 110,  79, 113, 224, 232, 178, 185, 112, 104,
                218, 246,  97, 228, 251,  34, 242, 193, 238, 210, 144,  12, 191, 179, 162, 241,
                81,   51, 145, 235, 249,  14, 239, 107,  49, 192, 214,  31, 181, 199, 106, 157,
                184,  84, 204, 176, 115, 121,  50,  45, 127,   4, 150, 254, 138, 236, 205,  93,
                222, 114,  67,  29,  24,  72, 243, 141, 128, 195,  78,  66, 215,  61, 156, 180
            ]
        ) # Ken Perlin's original permutation table
        self._gradients = np.array(list(zip(np.zeros(256), np.zeros(256))))
        # print(self._permutations)
        # print(self._gradients)
        random.seed(seed)
        # predefined randomized gradients
        for g in self._gradients:
            g[0], g[1] = random.randint(-127, 127), random.randint(-127, 127)
            length = math.sqrt(g[0]**2 + g[1] ** 2)
            g[0], g[1] = g[0] / length, g[1] / length
        # print(self._permutations)
        #  print(self._gradients)

    def lerp(self, t, a, b ): # linear interpolation function
    
        return a + t*( b - a )
    
    
    def s_curve(self, t ): # shaped blending function
         return t*t*(3-2*t)
    

    def random_vector_2d_fast(self,x,y) -> tuple[int,int]: # A Pseudorandom function using the predefined permutations originating from the seed
        i = self._permutations[x & 255]
        j = self._permutations[(y+i) & 255]
        # print(tuple(self._gradients[int(j)]))
        return tuple(self._gradients[int(j)])

    def perlin_noise2D(self, x: int, y: int) -> float: # perlin noise function 


        g = self.random_vector_2d_fast(x, y)
        v = (x - g[0], y - g[1])
        #  print (g[0] * v[0])
        return g[0] * v[0] + g[1] * v[1]

    def smooth_noise2D(self, x: float, y: float): # interpolated perlin noise function
    
        #  xi,yi; //integer component
        #  xf,yf; //floating point component
        #  xs,ys; //s-curve function results
        #  l00, l01, l10, l11; //uninterpolated values
        #  l0, l1; //partially interpolated values
        xi = int(x)
        xf = x - float(xi)
        xs = self.s_curve(xf)
        yi = int(y)
        yf = y - float(yi)
        ys = self.s_curve(yf)
        l00 = self.perlin_noise2D( xi , yi )
        l01 = self.perlin_noise2D( xi+1, yi )
        l10 = self.perlin_noise2D( xi , yi+1 )
        l11 = self.perlin_noise2D( xi+1, yi+1 )
        l0 = l00*l01 + l10*l11 # calculate dot product

        l0 = l00*l01 + l10*l11 # calculate dot product
        
    def block_height(self, x: np.ndarray, y: np.ndarray):
        h = (np.sin(x/24)*np.sin(y/24)+1)/2*256 # Takes in an array
        return h.astype(np.uint8)
    def generate_chunk_heights(self,x,y):
        # Create a local coordinate grid at (x,y)
        x_coords, y_coords = np.indices((16,16))
        world_x_coords = x_coords + 16*x
        world_y_coords = y_coords + 16*y
        heights = self.block_height(world_x_coords, world_y_coords)
        #print(heights)
        
        return heights.astype(np.uint8)


    
    def generate_chunk(self, chunk_x, chunk_z):
        """generates a np array shape [256, 16 16] at given chunk coords
        
        0 = air
        1 = stone
        ... More to come...
        
        """
        chunk_heights = self.generate_chunk_heights(chunk_x, chunk_z)
        increasing_subtraction = np.arange(256, dtype=np.int16)[:,None,None] # Shapes into 3d
        slices = chunk_heights[None,:,:] - increasing_subtraction # it is the chunk height at every x,z cord at each Y cord
        print(slices[0])
        print(slices[1])
        print(slices[255])
        slices = np.astype((slices>0), np.uint8)
        print(slices[0])
        print(slices[150])




if __name__ == "__main__": # debug
    
    from PIL import Image, ImageDraw
    # COLOR_BANDS = {
    #     0: (0,0,0), # deep ocean
    #     60: (10min(255, max(0, (self.smooth_noise2D((x+0.5)/10.2, (y+0.5)/10.2)) / 1000)), 30, 210), # shallow water
    #     61: (190, 180, 10), # beach
    #     65: (190, 180, 10), # beach
    #     69: (50, 200, 20), # Grass
    #     150: (50, 200, 20), # Grass
    #     200: (100, 100, 100),
    #     255: (150, 150, 150)

    # }

    # # COLOR_BANDS = [
    # #            [0, (0,0,100)], # deep ocean
    # #           [60, (10, 30, 210)], # shallow water
    # #           [61, (190, 180, 10)], # beach
    # #           [65, (190, 180, 10)], # beach
    # #           [69, (50, 200, 20)], # Grass
    # #          [150, (50, 200, 20)], # Grass
    # #          [200, (100, 100, 100)],
    # #          [255, (150, 150, 150)]
    
    # #     ]
    # # colours = []
    # yvals = list(COLOR_BANDS.values())
    # for y in range(255):
    #     closest_yval_index = min([abs(abs(yvals[i])-y) for i in len(yvals)])

    #     print(y, yvals[closest_yval_index])

    options = {
        "cells": [
            [1024, 255]
        ],
    }
    random.seed()
    seed = random.randint(0,122)
    #print(seed)
    tgen = TerrainGenerator(seed, options)
    tgen.generate_chunk(0,0)
    # print(tgen.smooth_noise2D(12.1, 20.1))
    # print(tgen.smooth_noise2D(14.1, 20.1))
    im = Image.new("L", (255, 255))
    # d = ImageDraw.Draw(im, "L")
    for x in range(16):
        for y in range(16):
            
            chunk = tgen.generate_chunk_heights(x,y)
            chunk_image = Image.fromarray(chunk, "L")
            offset = (16*x, 16*y)
            im.paste(chunk_image, offset)

    im.show()
