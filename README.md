# search_algorithm
### Different search algoruthm to find path in a maze

目前有A*算法、BFS、DFS、Dijkstra和GBFS（贪婪最佳优先）。



#### 文件

`random_map.py`包含了节点类和地图类，有随机地图与固定地图2种；

`search_algorithm.py`包含了`AStar`类，即A*算法；`BFS`类，即BFS算法……

`main.py`为入口文件。



#### 使用

使用方法：运行`main.py`即可。

使用matplotlib的交互模式，实现搜索节点时的map动态刷新功能。

最终保存寻找到的路径图片到img文件夹。



#### 样例

##### A*

代价函数 $ f(n) = g(n)+h(n) $ ，其中`g(n) = x_dis + y_dis + round(float((math.sqrt(2) - 2)*min(x_dis, y_dis)), 3)`即对角距离，使用对角距离是为了控制路线靠近中心线，`h(n) = x_dis + y_dis `即曼哈顿距离。

<img src="img/AStar.png" alt="A*示例" style="zoom:70%;" />

蓝色+绿色为经过的点，绿色为回溯时寻找的路径。

##### BFS

<img src="img/BFS.png" alt="BFS示例" style="zoom:60%;" />

##### DFS

<img src="img/DFS.png" alt="DFS示例" style="zoom:60%;" />

##### Dijkstra

<img src="img/Dijkstra.png" alt="Dijkstra示例" style="zoom:60%;" />

由于格子之间的路径是一致的，所以看起来会和BFS一样。

##### GBFS

<img src="img/GBFS.png" alt="GBFS示例" style="zoom:60%;" />

TODO：

- [x] BFS
- [x] DFS
- [x] Dijkstra
- [x] GBFS

