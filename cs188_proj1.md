#! https://zhuanlan.zhihu.com/p/569252307
# UCB cs188: 人工智能导论 | Proj 1 搜索
本文为本人实现 `cs188` proj 的课程笔记,只是用于记录解题过程.
如需要系统学习人工智能,请看官方文档

## 第一部分 使用 `DFS` 为吃豆人 寻路

最初我的想法是,在寻路过程中,记录吃豆人的移动方向.但在实际运行之后发现
这样编写算法需要进行回溯,因为如果一条道走不通,吃豆人必须要原路返回到
最开始的 `分叉路口`,才能接着探下一条路.

那不如就先寻路,找到正确路径后,再让吃豆人移动, 一次成功.
为了能够抵达终点时,可以复原路径.为此我构造了一个搜索节点
```python
class serNode:
    def __init__(self, prior, pos, action, expense=0,cost=0) -> None:
        self.prior = prior
        self.pos = pos
        self.action = action
        self.expense = expense
        self.cost = cost
    
    def getPrior(self):
        return self.prior
   
    def getPos(self):
        return self.pos
  
    def getAction(self):
        return self.action
            
    def getExpense(self):
        return self.expense

    def getF(self):
        return self.cost
```
- `prior` 指向上一个节点
- `pos` 是节点当前的位置,用于生成 `Successors`
- `action` 是从上一个状态 转换为 当前状态所需的动作

通过 `prior` 指针,我们就可以从终点回溯到起点,获取到一条通路

第二部分 BFS 算法 寻路,第三部分 UCS 算法 寻路与第一部分基本相同,不再赘述

## 第四部分 A* 算法 寻路

初步算法实现上与第一部分没啥差别,将 fringe 的数据类型从栈 换成 **优先队列** 即可.
但是在运行 autograder.py 的时候,这个 test case 一直 fail

```
*** FAIL: test_cases\q4\astar_3_goalAtDequeue.test
***     graph:
***             1      1      1
***         *A ---> B ---> C ---> [G]
***          |                     ^
***          |         10          |
***          \---------------------/
***
***         A is the start state, G is the goal.  Arrows mark possible state
***         transitions.  The number next to the arrow is the cost of that transition.
***
***         If you fail this test case, you may be incorrectly testing if a node is a goal
***         before adding it into the queue, instead of testing when you remove the node
***         from the queue.  See the algorithm pseudocode in lecture.
***     student solution:               ['0:A->G']
***     student expanded_states:        ['A', 'B', 'C']
***
***     correct solution:               ['1:A->B', '0:B->C', '0:C->G']
***     correct expanded_states:        ['A', 'B', 'C']
***     correct rev_solution:           ['1:A->B', '0:B->C', '0:C->G']
***     correct rev_expanded_states:    ['A', 'B', 'C']
```
这个提示说:我将节点加入fringe的时候,就已经将其标记为访问过l,这是不正确的,仅当节点从fringe 弹出时
才能标记该节点为访问过

原因见下
> In other words, if you DO attempt to do this, you should only "mark" a WorldState when it is dequeued from the PQ, not when it is enqueued! The reason for this is beyond the scope of 61B (see CS188 for more!), but the rough intuition behind this is as follows: If you're at a move sequence (a.k.a. SearchNode) that ends at WorldState X and you see that WorldState G is one of X's neighbors, it's not safe to assume that this is the best path, and therefore it's not safe to enqueue X->G and then subsequently disallow all other paths that end in G.

- 修复了这个bug 后,又有个test case fail了
```
*** FAIL: test_cases\q4\graph_manypaths.test
***     graph:
***             B1          E1
***            ^  \        ^  \
***           /    V      /    V
***         *A --> C --> D --> F --> [G]
***           \    ^      \    ^
***            V  /        V  /
***             B2          E2
***
***         A is the start state, G is the goal.  Arrows mark
***         possible state transitions.  This graph has multiple
***         paths to the goal, where nodes with the same state
***         are added to the fringe multiple times before they
***         are expanded.
***     student solution:               ['1:A->C', '0:C->D', '1:D->F', '0:F->G']
***     student expanded_states:        ['A', 'B1', 'C', 'B2', 'C', 'D', 'D', 'E1', 'E1', 'F', 'F', 'E2', 'E2', 'F', 'F']
***
***     correct solution:               ['1:A->C', '0:C->D', '1:D->F', '0:F->G']
***     correct expanded_states:        ['A', 'B1', 'C', 'B2', 'D', 'E1', 'F', 'E2']
***     correct rev_solution:           ['1:A->C', '0:C->D', '1:D->F', '0:F->G']
***     correct rev_expanded_states:    ['A', 'B1', 'C', 'B2', 'D', 'E1', 'F', 'E2']
*** Tests failed.
```
问题解决
完成proj part 1-4

之前存在的问题:

<<<<

不是判断 从fringe 中弹出的元素 是否访问过
而是判断 从fringe 中弹出元素节点的后续节点 有没有访问过

\>\>\>\>

而实际上需要先判断 从fringe弹出的元素是否访问过
如果访问过, 那么我们就不做任何操作.

```python
if top.pos not in visited_state:
    visited_state.add(top.pos)
    for n in problem.getSuccessors(top.pos):
        fringe.push(serNode(top, n[0], n[1], n[2], top.cost + n[2]), 
            top.cost + n[2])
```
## 第五部分
这一部分要求对一个搜索问题进行建模--如何最快吃到四个角落的食物

- 如何判断当前位置是否为目标位置呢
  - 设定一个储存了四个角落的集合
  - 每次进行 `isGoal` 判断的时候,判断当前位置是否在这个集合中,如果在,删去集合中的这个元素,当集合为空时,说明四个角落到去过了,搜索结束
- 问题:bfs 确实能够寻找到四个角落,但是没法输出正确的路径
  - 原因:这样找到的是从起点到四个角落的四条路径,而不是一条抵达四个角落的最短路径 
- 解决方案 (参考github上 zhiming 的解决方案)
  - 跟踪每一个节点的路径:在进行 `is Goal` 节点判断的时候,我们只需要查看当前节点的路径是否覆盖了四个角落即可

在这个问题中, state储存的不仅是 pacman 的状态, 还有是否去过四个角落的标志位
```python
class searchState:
    
    def __init__(self, state, corners: Tuple, visited: List) -> None:
        self.stat = state
        self.visited = visited
        self.map = self.do_zip(corners, visited) 
    
    def __repr__(self) -> str:
        return "{0}{1}".format(self.stat, self.visited)
    
    def __eq__(self, __o) -> bool:
        return isinstance(__o, searchState) and self.stat == __o.stat \
            and self.visited == __o.visited
    
    def __hash__(self) -> int:
        return hash((self.stat, self.visited[0],
                    self.visited[1], self.visited[2], self.visited[3]))
    
    def do_zip(self, corners: Tuple, visited: List)-> Dict:
        dic = {}
        for i, j in zip(corners, visited):
            dic[i] = j
        return dic
    
    def isVisitedAll(self) -> Boolean:
        assert isinstance(self.map, Dict)
        return all(list(self.map.values()))
 
```

## 第六部分
为part 5 的搜素问题写一个启发式函数:
我的解决方案是 将尚未访问的节点中，距离pacman 哈密顿距离的最大值 作为启发式函数的值
```python
def calCost(state: Tuple, lst: List):
    x1, y1 = state
    cost_list = [ abs(x1 - l[0]) + abs(y1-l[1]) for l in lst ]
    return max(cost_list) 
```
## 第七部分
与第六部分思路一样，最后展开了 9551 个节点，完成度 3 / 4

## 第八部分 
greedy search

ClosestDotSearchAgent
    registerInitialState 检验路径正确性
        findPathToClosestDot 找到针对最短节点的路径

AnyFoodSearchProblem
    Goal findClosetDot
     explain the getFood of gamestate
     how to find the bound of the grid

最初的设想：
    1. 使用 mazeDistance 遍历所有的 food，找到距离当前位置最近的food
    2. 用bfs 求得 到这个food的 距离，并返回
但这样太慢了。

我们可以对 AnyFoodSearchProblem goal state 的 目标条件更改为
**只要当前PACMAN所在的位置有食物**，就计算为找到目标

    