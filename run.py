import os
import sys

if __name__ == "__main__":
    # Ensure dependencies are installed (optional, but good for local run)
    # try:
    #     import pygame
    # except ImportError:
    #     os.system(sys.executable + " -m pip install pygame-ce")

    # Run the game
    os.system(sys.executable + " -m python_bomberman.main")
