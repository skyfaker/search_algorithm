import numpy as np
import sys


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        # g_cost为当前点与起点的移动代价，使用对角距离
        self.g_cost = sys.maxsize
        # f_cost为总的代价函数，为g_cost+当前点与终点的曼哈顿距离
        self.f_cost = sys.maxsize


class RandomMap:
    """
    生成随机地图，默认地图30*30
    """

    def __init__(self, size=30):  # 默认地图
        self.size = size
        self.obstacle = size // 3
        self.GenerateObstacle()

    # 生成障碍物
    def GenerateObstacle(self):
        self.obstacle_point = []
        self.obstacle_point.append(Point(self.size // 2, self.size // 2))
        self.obstacle_point.append(Point(self.size // 2, self.size // 2 - 1))

        # Generate an obstacle in the middle
        for i in range(self.size // 2 - (self.size // 10) - 1, self.size // 2):
            self.obstacle_point.append(Point(i, self.size - i))
            self.obstacle_point.append(Point(i, self.size - i - 1))
            self.obstacle_point.append(Point(self.size - i, i))
            self.obstacle_point.append(Point(self.size - i, i - 1))

        # 生成随机横向或者纵向障碍
        for i in range(self.obstacle):
            x = np.random.randint(0, self.size)
            y = np.random.randint(0, self.size)
            self.obstacle_point.append(Point(x, y))

            if np.random.rand() > 0.5:  # Random boolean
                for r in range(self.size // 3):
                    if y+r<self.size:
                        self.obstacle_point.append(Point(x, y + r))
            else:
                for r in range(self.size // 3):
                    if x+r<self.size:
                        self.obstacle_point.append(Point(x + r, y))

    # 判斷是否障碍物
    def IsObstacle(self, i, j):
        for p in self.obstacle_point:
            if i == p.x and j == p.y:
                return True
        return False