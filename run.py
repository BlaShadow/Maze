#! run file

from config import config
from maze import Maze
from slave import Slave

maze = Maze(config)

if __name__ == '__main__':
	maze.play()


