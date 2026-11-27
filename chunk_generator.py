import pyray as pr
import raylib as pr_const # raylib in python is unfinsihed and some of hte C bindings are still essential to use.
import terrain_generator as tg
import numpy as np


TEXTURE_SIZE = 16

TEXTURES = {
            0: None, # air
            1: ((0,0), (0,0), (0,0), (0,0), (0,0), (0,0)), # stone shape per face 
        }


class ChunkGenerator():
    """
    
    how it'll work
    define a chunk grid as a [256,16,16 array]
    for each block that isnt air (>0)
    generate a vertices array
    edges array
    faces array
    with uv coords from tmap (256x256 grid)
    """
    def __init__(self, seed=0):
        self.tgen = tg.TerrainGenerator(
                seed=seed,
                world_gen_options={

                }
            )
          
    def get_mesh(self, chunk_x, chunk_z):

        """Step 0: generate the actual chunk"""
        block_map = self.tgen.generate_empty_chunk(chunk_x,chunk_z) # (256,16,16), uint8
        print(np.shape(block_map))
        """
        Step 1: remove all blocks that are not touching air and make array of (shape 10 4)
        """

        # Touching Filter

        # array making

        block_list = np.argwhere(block_map != 0)
        type_list = block_map[block_list]
        print("bl", block_list)
        print("tl", type_list)
        """
        Step 2: get all vertices of blocks and uvs
        """


        


if __name__ == "__main__":
    cgen = ChunkGenerator()
    cgen.get_mesh(0,0)