import pyray as pr
import raylib as pr_const # raylib in python is unfinsihed and some of hte C bindings are still essential to use.
import terrain_generator as tg


class ChunkGenerator():
    """
    
    how it'll work
    define a chunk grid as a 16x16 grid
    define vertex order (always ccw around top)
    np grid
        [
            (0, tgen..height, 0)
        ]
    
    """
    def __init__(self, seed):
