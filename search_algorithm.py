# a_star.py

import sys
import time
import numpy as np
from matplotlib.patches import Rectangle
import random_map 
import math


class AStar:
    def __init__(self, map):
        self.map = map
        self.open_set = []
        self.close_set = []

    # 节点到起点的移动代价：曼哈顿距离
    def BaseCost(self, p):
        x_dis = abs(p.x - 0)
        y_dis = abs(p.y - 0)
        # Distance to start point
        return x_dis + y_dis + round((math.sqrt(2) - 2)*min(x_dis, y_dis), 1)

    # 节点到终点的启发函数
    def HeuristicCost(self, p):
        x_dis = abs(self.map.size - 1 - p.x)
        y_dis = abs(self.map.size - 1 - p.y)
        # Distance to end point
        return 2 * (x_dis + y_dis)

    def TotalCost(self, p):
        return self.BaseCost(p) + self.HeuristicCost(p)

    # 判断点是否有效，不在地图内部或者障碍物所在点都是无效的。
    def IsValidPoint(self, x, y):
        if x < 0 or y < 0:
            return False
        if x >= self.map.size or y >= self.map.size:
            return False
        return not self.map.IsObstacle(x, y)

    def IsInPointList(self, p, point_list):
        for point in point_list:
            if point.x == p.x and point.y == p.y:
                return True
        return False

    def IsInOpenList(self, p):
        return self.IsInPointList(p, self.open_set)

    def IsInCloseList(self, p):
        return self.IsInPointList(p, self.close_set)

    def IsStartPoint(self, p):
        return p.x == 0 and p.y == 0

    def IsEndPoint(self, p):
        return p.x == self.map.size - 1 and p.y == self.map.size - 1

    def RunAndSaveImage(self, ax, plt):

        start_time = time.time()

        start_point = random_map.Point(0, 0)
        start_point.g_cost = 0
        start_point.f_cost = 0
        self.open_set.append(start_point)

        while True:
            index = self.SelectPointInOpenList()
            if index < 0:
                print('No path found, algorithm failed!!!')
                return
            p = self.open_set[index]
            rec = Rectangle((p.x, p.y), 1, 1, color='c')
            ax.add_patch(rec)
            
            # plt.draw()
            plt.pause(0.05)
            
            # self.SaveImage(plt)

            if self.IsEndPoint(p):
                return self.BuildPath(p, ax, plt, start_time)

            del self.open_set[index]
            self.close_set.append(p)

            # Process all neighbors
            x = p.x
            y = p.y
            # 启发函数为曼哈顿距离，可以遍历上下左右4个点
            self.ProcessPoint(x-1, y, p)
            self.ProcessPoint(x, y-1, p)
            self.ProcessPoint(x+1, y, p)
            self.ProcessPoint(x, y+1, p)

            # 对角距离8个点
            # self.ProcessPoint(x-1, y+1, p)
            # self.ProcessPoint(x-1, y, p)
            # self.ProcessPoint(x-1, y-1, p)
            # self.ProcessPoint(x, y-1, p)
            # self.ProcessPoint(x+1, y-1, p)
            # self.ProcessPoint(x+1, y, p)
            # self.ProcessPoint(x+1, y+1, p)
            # self.ProcessPoint(x, y+1, p)

    # 保存图片
    def SaveImage(self, plt):
        millis = int(round(time.time() * 1000))
        filename = './img/' + str(millis) + '.png'
        plt.savefig(filename)

    # 算法关键点：判断邻点的状态，以选择下一个要遍历的点
    def ProcessPoint(self, x, y, parent):
        # 不合法的点
        if not self.IsValidPoint(x, y):
            return # Do nothing for invalid point
        p = random_map.Point(x, y)

        # 邻点在close_set中，跳过
        if self.IsInCloseList(p):
            return # Do nothing for visited point
        
        # 邻点p在open_set，比较g(n)是否比原来更小，如果更小则更新其g(n)、优先级f(n)和其父节点
        if self.IsInOpenList(p):
            path = self.BaseCost(p)
            if path < parent.g_cost+1:
                p.parent = parent
            p.g_cost = path
            p.f_cost = self.TotalCost(p)

        # 邻点p既不在open_set，也不在close_set中，设置节点p的parent为节点n，计算节点p的优先级f(n)，将节点m加入open_set中
        else:
            p.parent = parent
            p.g_cost = self.BaseCost(p)
            p.f_cost = self.TotalCost(p)
            self.open_set.append(p)

        print('Process Point [', p.x, ',', p.y, ']', ', f_cost: ', p.f_cost)

    # 选取TotalCost最小的点，这里直接遍历，没有使用最小堆
    # TODO：换成最小堆
    def SelectPointInOpenList(self):
        index = 0
        selected_index = -1
        min_cost = sys.maxsize
        for p in self.open_set:
            # cost = self.TotalCost(p)
            cost = p.f_cost
            if cost < min_cost:
                min_cost = cost
                selected_index = index
            index += 1
        return selected_index

    # 回溯寻找路径，并绘制出来
    def BuildPath(self, p, ax, plt, start_time):
        path = []
        while True:
            path.insert(0, p) # Insert first
            if self.IsStartPoint(p):
                break
            else:
                p = p.parent
        for p in path:
            rec = Rectangle((p.x, p.y), 1, 1, color='g')
            ax.add_patch(rec)
            plt.draw()
        self.SaveImage(plt)
        end_time = time.time()

        # 时间较长为绘图的原因
        print('===== Algorithm finish in', end_time-start_time, ' seconds')