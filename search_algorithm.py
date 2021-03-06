# a_star.py

import sys
import time
import numpy as np
from matplotlib.patches import Rectangle
import random_map 
import math


# 父类，定义子类公用方法
class search_algorithm:
    def __init__(self, map):
        self.map = map
        self.open_set = []
        self.close_set = []

    # 判断点是否有效，不在地图内部或者障碍物所在点都是无效的。
    def IsValidPoint(self, x, y):
        if x < 0 or y < 0:
            return False
        if x >= self.map.size or y >= self.map.size:
            return False
        return not self.map.IsObstacle(x, y)

    # 判断点是否在open_set中，如果在，则返回这个点，这样可以便于之后修改点的属性。因为此时传入的参数p是值传递
    def IsInOpenList(self, p):
        for point in self.open_set:
            if point.x == p.x and point.y == p.y:
                return point
        return False

    def IsInCloseList(self, p):
        for point in self.close_set:
            if point.x == p.x and point.y == p.y:
                return True
        return False

    def IsStartPoint(self, p):
        return p.x == 0 and p.y == 0

    def IsEndPoint(self, p):
        return p.x == self.map.size - 1 and p.y == self.map.size - 1

    # 保存图片
    def SaveImage(self, plt, baseName):
        millis = int(round(time.time()))
        filename = './img/' + baseName + str(millis) + '.png'
        plt.savefig(filename)

        # 回溯寻找路径，并绘制出来
    
    def BuildPath(self, p, ax, plt, start_time, baseName):
        path = []
        while True:
            path.insert(0, p) # Insert first
            if self.IsStartPoint(p):
                break
            else:
                p = p.parent
        for p in path[1:-1]:
            rec = Rectangle((p.x, p.y), 1, 1, color='lightgreen')
            ax.add_patch(rec)
        plt.draw()
        plt.pause(1)
        self.SaveImage(plt, baseName)
        end_time = time.time()

        # 时间较长为绘图的原因
        print('===== Algorithm finish in', end_time-start_time, ' seconds')
        print('===== 路径长度：{}'.format(len(path)))

    def getMaxAreaPoint(self, p):
        return max(abs(self.map.size - 1 - p.x), abs(self.map.size - 1 - p.y))

class AStar(search_algorithm):
    def __init__(self, map):
        self.map = map
        self.open_set = []
        self.close_set = []

    # 节点到起点的移动代价：对角距离，是为了让路径更靠近中心线；已经做了兼容，可以直接改成曼哈顿距离，这样就会让路径沿着边缘。
    def BaseCost(self, p):
        x_dis = abs(p.x - 0)
        y_dis = abs(p.y - 0)
        # Distance to start point
        # return x_dis + y_dis + round(float((math.sqrt(2) - 2)*min(x_dis, y_dis)), 3)
        return x_dis + y_dis

    # 节点到终点的启发函数：曼哈顿距离
    def HeuristicCost(self, p):
        x_dis = abs(self.map.size - 1 - p.x)
        y_dis = abs(self.map.size - 1 - p.y)
        # Distance to end point
        return (x_dis + y_dis)

    def TotalCost(self, p):
        return self.BaseCost(p) + self.HeuristicCost(p)
        # return p.g_cost + self.HeuristicCost(p)

    # 选取TotalCost最小的点，这里直接遍历，没有使用最小堆
    # TODO：换成最小堆
    def SelectPointInOpenList(self):
        index = 0
        selected_index = -1
        min_cost = sys.maxsize
        for p in self.open_set:
            cost = p.f_cost
            # if cost < min_cost:
            #     min_cost = cost
            #     selected_index = index
            # 在代价函数相同时，优先选择g(n)最小的点
            # elif cost == min_cost and p.g_cost < self.open_set[selected_index].g_cost:
            #     min_cost = cost
            #     selected_index = index

            if cost < min_cost:
                min_cost = cost
                selected_index = index
            # 在代价函数相同时，优先选择与终点组成的矩形面积最大的点
            elif cost == min_cost:
                if self.getMaxAreaPoint(p) < self.getMaxAreaPoint(self.open_set[selected_index]):
                    min_cost = cost
                    selected_index = index

            index += 1
        return selected_index

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
        # 这里可以删除open_set中的对应点，修改后重新加入；也可以调用函数返回这个点然后对其修改
        open_p = self.IsInOpenList(p)
        if open_p:
            p = open_p
            # 比较该点前一次遍历的点和该点的父节点的g_cost，前一个遍历点小则更新父节点为前一个遍历点
            if parent.g_cost < p.parent.g_cost:
                p.parent = parent
                p.g_cost = self.BaseCost(p)
                # p.g_cost = parent.g_cost + 1
                p.f_cost = self.TotalCost(p)

        # 邻点p既不在open_set，也不在close_set中，设置节点p的parent为节点n，计算节点p的优先级f(n)，将节点m加入open_set中
        else:
            p.parent = parent
            p.g_cost = self.BaseCost(p)
            # p.g_cost = parent.g_cost + 1
            p.f_cost = self.TotalCost(p)
            self.open_set.append(p)

        print('Process Point [', p.x, ',', p.y, ']', ', f_cost: ', p.f_cost)

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
            
            if (not (p.x==0 and p.y==0)) and (not (p.x==self.map.size-1 and p.y==self.map.size-1)):
                rec = Rectangle((p.x, p.y), 1, 1, color='c')
                ax.add_patch(rec)
            
                # plt.draw()
                plt.pause(0.05)
            # self.SaveImage(plt)

            if self.IsEndPoint(p):
                return self.BuildPath(p, ax, plt,start_time, baseName="AStar")

            del self.open_set[index]
            self.close_set.append(p)

            # Process all neighbors
            x = p.x
            y = p.y
            # 启发函数为曼哈顿距离，可以遍历上右下左4个点
            self.ProcessPoint(x+1, y, p)
            self.ProcessPoint(x, y+1, p)
            self.ProcessPoint(x-1, y, p)
            self.ProcessPoint(x, y-1, p)

            # 允许从对=对角走的话可以遍历8个点
            # self.ProcessPoint(x-1, y+1, p)
            # self.ProcessPoint(x-1, y, p)
            # self.ProcessPoint(x-1, y-1, p)
            # self.ProcessPoint(x, y-1, p)
            # self.ProcessPoint(x+1, y-1, p)
            # self.ProcessPoint(x+1, y, p)
            # self.ProcessPoint(x+1, y+1, p)
            # self.ProcessPoint(x, y+1, p)


class BFS(search_algorithm):
    def __init__(self, map):
        self.map = map
        self.open_set = []
        self.close_set = []
    
    def SelectPointInOpenList(self):
        if len(self.open_set)==0:
            return None
        p = self.open_set.pop(0)
        return p

    def ProcessPoint(self, x, y, parent):
        # 不合法的点，不做处理
        if not self.IsValidPoint(x, y):
            return
        p = random_map.Point(x, y)

        # 邻点在close_set和open_set中，跳过
        if self.IsInCloseList(p) or self.IsInOpenList(p):
            return # Do nothing for visited point

        else:
            p.parent = parent
            self.open_set.append(p)
        print('Process Point [', p.x, ',', p.y, ']')

    def RunAndSaveImage(self, ax, plt):
        start_time = time.time()

        start_point = random_map.Point(0, 0)
        self.open_set.append(start_point)

        while True:
            p = self.SelectPointInOpenList()
            if not p:
                print('No path found, algorithm failed!!!')
                return
                      
            if (not (p.x==0 and p.y==0)) and (not (p.x==self.map.size-1 and p.y==self.map.size-1)):                        
                rec = Rectangle((p.x, p.y), 1, 1, color='c')
                ax.add_patch(rec)
        
                # plt.draw()
                # plt.pause(0.05)

            if self.IsEndPoint(p):
                return self.BuildPath(p, ax, plt, start_time, baseName="BFS")
            
            self.close_set.append(p)

            # Process all neighbors
            x = p.x
            y = p.y
            # 启发函数为曼哈顿距离，可以遍历上下左右4个点
            self.ProcessPoint(x-1, y, p)
            self.ProcessPoint(x, y-1, p)
            self.ProcessPoint(x+1, y, p)
            self.ProcessPoint(x, y+1, p)


class DFS(search_algorithm):
    def __init__(self, map):
        self.map = map
        self.open_set = []
        self.close_set = []
    
    def SelectPointInOpenList(self):
        if len(self.open_set)==0:
            return None
        p = self.open_set.pop(-1)
        return p

    def ProcessPoint(self, x, y, parent):
        # 不合法的点，不做处理
        if not self.IsValidPoint(x, y):
            return
        p = random_map.Point(x, y)

        # 邻点在close_set和open_set中，跳过
        if self.IsInCloseList(p) or self.IsInOpenList(p):
            return # Do nothing for visited point

        else:
            p.parent = parent
            self.open_set.append(p)
        print('Process Point [', p.x, ',', p.y, ']')

    def RunAndSaveImage(self, ax, plt):
        start_time = time.time()

        start_point = random_map.Point(0, 0)
        self.open_set.append(start_point)

        while True:
            p = self.SelectPointInOpenList()
            if not p:
                print('No path found, algorithm failed!!!')
                return
                      
            if (not (p.x==0 and p.y==0)) and (not (p.x==self.map.size-1 and p.y==self.map.size-1)):                        
                rec = Rectangle((p.x, p.y), 1, 1, color='c')
                ax.add_patch(rec)
        
                # plt.draw()
                plt.pause(0.05)

            if self.IsEndPoint(p):
                return self.BuildPath(p, ax, plt, start_time, baseName="DFS")
            
            self.close_set.append(p)

            # Process all neighbors
            x = p.x
            y = p.y
            # 启发函数为曼哈顿距离，遍历下左上右4个点
            # 因为终点在右上方，所以优先向上和右遍历
            self.ProcessPoint(x, y-1, p)
            self.ProcessPoint(x-1, y, p)
            self.ProcessPoint(x+1, y, p)
            self.ProcessPoint(x, y+1, p)


class Dijkstra(search_algorithm):
    def __init__(self, map):
        self.map = map
        self.open_set = []
        self.close_set = []

    # 节点到起点的移动代价：对角距离，是为了让路径更靠近中心线；已经做了兼容，可以直接改成曼哈顿距离，这样就会让路径沿着边缘。
    def BaseCost(self, p):
        x_dis = abs(p.x - 0)
        y_dis = abs(p.y - 0)
        # Distance to start point
        return x_dis + y_dis + round(float((math.sqrt(2) - 2)*min(x_dis, y_dis)), 3)
        # return x_dis + y_dis

    # 选取代价函数最小的点，此时代价函数为起点到当前点的距离g(n)
    # 这里最好返回index而不是点，方便之后使用del删除
    def SelectPointInOpenList(self):
        index = 0
        selected_index = -1
        min_cost = sys.maxsize
        for p in self.open_set:
            cost = p.g_cost
            if cost < min_cost:
                min_cost = cost
                selected_index = index
            index += 1
        return selected_index

    def ProcessPoint(self, x, y, parent):
        # 不合法的点，不做处理
        if not self.IsValidPoint(x, y):
            return
        p = random_map.Point(x, y)

        # 邻点在close_set，跳过
        if self.IsInCloseList(p):
            return # Do nothing for visited point

        open_p = self.IsInOpenList(p)
        if open_p:
            p = open_p
            if p.parent and parent.g_cost < p.parent.g_cost:
                p.parent = parent
                # p.g_cost = parent.g_cost + 1
                p.g_cost = self.BaseCost(p)


        else:
            p.parent = parent
            p.g_cost = self.BaseCost(p)
            self.open_set.append(p)
        print('Process Point [', p.x, ',', p.y, ']')

    def RunAndSaveImage(self, ax, plt):
        start_time = time.time()
        start_point = random_map.Point(0, 0)
        start_point.g_cost = 0
        self.open_set.append(start_point)

        while True:
            index = self.SelectPointInOpenList()
            if index < 0:
                print('No path found, algorithm failed!!!')
                return

            p = self.open_set[index]
            del self.open_set[index]

            if (not (p.x==0 and p.y==0)) and (not (p.x==self.map.size-1 and p.y==self.map.size-1)):                        
                rec = Rectangle((p.x, p.y), 1, 1, color='c')
                ax.add_patch(rec)
        
                # plt.draw()
                plt.pause(0.05)

            if self.IsEndPoint(p):
                return self.BuildPath(p, ax, plt, start_time, baseName="Dijkstra")
            
            self.close_set.append(p)

            # Process all neighbors
            x = p.x
            y = p.y
            # 启发函数为曼哈顿距离，遍历下左上右4个点
            # 因为终点在右上方，所以优先向上和右遍历
            self.ProcessPoint(x, y-1, p)
            self.ProcessPoint(x-1, y, p)
            self.ProcessPoint(x+1, y, p)
            self.ProcessPoint(x, y+1, p)

class GBFS(search_algorithm):
    def __init__(self, map):
        self.map = map
        self.open_set = []
        self.close_set = []

    # 节点到终点的启发函数：对角距离，使得路径沿着中心线
    def HeuristicCost(self, p):
        x_dis = abs(self.map.size - 1 - p.x)
        y_dis = abs(self.map.size - 1 - p.y)
        # Distance to end point
        # return x_dis + y_dis + round(float((math.sqrt(2) - 2)*min(x_dis, y_dis)), 3)
        return (x_dis + y_dis)

    # 选取代价函数最小的点，此时代价函数为终点到当前点的距离f(n) = h(n)
    # 这里最好返回index而不是点，方便之后使用del删除
    def SelectPointInOpenList(self):
        index = 0
        selected_index = -1
        min_cost = sys.maxsize
        for p in self.open_set:
            cost = p.f_cost
            if cost < min_cost:
                min_cost = cost
                selected_index = index
            elif cost == min_cost:
                if self.getMaxAreaPoint(p) < self.getMaxAreaPoint(self.open_set[selected_index]):
                    min_cost = cost
                    selected_index = index
            index += 1
        return selected_index

    def ProcessPoint(self, x, y, parent):
        # 不合法的点，不做处理
        if not self.IsValidPoint(x, y):
            return
        p = random_map.Point(x, y)

        # 邻点在close_set，跳过
        if self.IsInCloseList(p) or self.IsInOpenList(p):
            return # Do nothing for visited point

        else:
            p.parent = parent
            p.f_cost = self.HeuristicCost(p)
            self.open_set.append(p)
        print('Process Point [', p.x, ',', p.y, ']')

    def RunAndSaveImage(self, ax, plt):
        start_time = time.time()
        start_point = random_map.Point(0, 0)
        start_point.f_cost = 0
        self.open_set.append(start_point)

        while True:
            index = self.SelectPointInOpenList()
            if index < 0:
                print('No path found, algorithm failed!!!')
                return

            p = self.open_set[index]
            del self.open_set[index]

            if (not (p.x==0 and p.y==0)) and (not (p.x==self.map.size-1 and p.y==self.map.size-1)):                        
                rec = Rectangle((p.x, p.y), 1, 1, color='c')
                ax.add_patch(rec)
        
                # plt.draw()
                plt.pause(0.05)

            if self.IsEndPoint(p):
                return self.BuildPath(p, ax, plt, start_time, baseName="GBFS")
            
            self.close_set.append(p)

            # Process all neighbors
            x = p.x
            y = p.y
            # 启发函数为曼哈顿距离，遍历下左上右4个点
            # 因为终点在右上方，所以优先向上和右遍历
            self.ProcessPoint(x, y-1, p)
            self.ProcessPoint(x-1, y, p)
            self.ProcessPoint(x+1, y, p)
            self.ProcessPoint(x, y+1, p)

