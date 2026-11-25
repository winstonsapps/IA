import pyray as pr
import raylib as pr_const # raylib in python is unfinsihed and some of hte C bindings are still essential to use.
import terrain_generator as tg


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
    def __init__(self, seed):
