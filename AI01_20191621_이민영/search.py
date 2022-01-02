###### Write Your Library Here ###########

import time
import itertools
from collections import defaultdict
from heapq import *
import queue as q
from copy import deepcopy
import sys

#########################################


def search(maze, func):
    return {
        "bfs": bfs,
        "astar": astar,
        "astar_four_circles": astar_four_circles,
        "astar_many_circles": astar_many_circles
    }.get(func)(maze)


# -------------------- Stage 01: One circle - BFS Algorithm ------------------------ #

def bfs(maze):
    """
    [문제 01] 제시된 stage1의 맵 세가지를 BFS Algorithm을 통해 최단 경로를 return하시오.(20점)
    """
    start_point=maze.startPoint()

    visited = []
    fringe = []
    path=[]
    # 값들 초기화하기 빈 리스트

    ####################### Write Your Code Here ################################
    
    fringe.append(start_point)
    def bf_Search():
        closed = []
        a = 1
        
        #finge안에 있는 node들 살펴보
        while fringe:
            node = fringe.pop(0)
            
            visited.append(node)
            for i in maze.neighborPoints(node[0],node[1]):
                if i not in visited:
                    #이웃노드들 중 아직 방문하지 않은 노드가 있으면 추가하
                    fringe.append(i)
                    
                    trace_path[i] = node
                    
            if maze.circlePoints == node:
                break

    '''최종 경로를 출력하기 위한 tracing함수 '''      
    def tracing(node,trace_path):
        
        if(node == maze.startPoint()):
            return
        index = node[0]*10+node[1]
       
        next_node = trace_path[node]
        tracing(next_node,trace_path)
        path.append(next_node)
    

    trace_path = dict()
    bf_Search()
    
    tracing(maze.circlePoints()[0],trace_path)
    path.append(maze.circlePoints()[0])
    


    return path

    ############################################################################



class Node:
    def __init__(self,parent,location):
        self.parent=parent
        self.location=location #현재 노드

        self.obj=[]

        # F = G+H
        self.f=0
        self.g=0
        self.h=0

    def __eq__(self, other):
        return self.location==other.location and str(self.obj)==str(other.obj)

    def __le__(self, other):
        return self.g+self.h<=other.g+other.h

    def __lt__(self, other):
        return self.g+self.h<other.g+other.h

    def __gt__(self, other):
        return self.g+self.h>other.g+other.h

    def __ge__(self, other):
        return self.g+self.h>=other.g+other.h


# -------------------- Stage 01: One circle - A* Algorithm ------------------------ #

def manhatten_dist(p1,p2):
    return abs(p1[0]-p2[0])+abs(p1[1]-p2[1])

def astar(maze):

    """
    [문제 02] 제시된 stage1의 맵 세가지를 A* Algorithm을 통해 최단경로를 return하시오.(20점)
    (Heuristic Function은 위에서 정의한 manhatten_dist function을 사용할 것.)
    """

    start_point=maze.startPoint()

    end_point=maze.circlePoints()[0]

    path=[]

    ####################### Write Your Code Here ################################

    def A_star():
        #초기화하기


        openlist = []
        closedlist=[]
        
        index = 0
      
        startN = Node(None,start_point)
        endN = Node(None,end_point)
        #살펴볼 노드를 openlist에 넣기  
        openlist.append(startN)
        while openlist:
           node = openlist[0]
           index = 0
           
           for i,j in enumerate(openlist):
        
               if j.f < node.f:
                   index = i
                   node = j
                   

          
           openlist.pop(index)
           closedlist.append(node)
           #목적지에 도달하면 return
           if node == endN:
               
                path = []
                now_N = node
                while now_N is not None:
                   path.append(now_N.location)
                   now_N = now_N.parent
                return path[::-1]


           child = []
           #이웃 노드들을 살펴보면서 child에 넣
           for i in maze.neighborPoints(node.location[0],node.location[1]):
               
                node_append = Node(node,i)
                child.append(node_append)
           
           for now_child in child:
                #child에 존재하는 노드들을 살펴보면서 g,h값을 이용해서 f 값구하기. h는 manhatten_dist를 이용하
                if now_child in closedlist:
                    
                    continue
                
                now_child.g = node.g + 1
                now_child.h = manhatten_dist(now_child.location,endN.location)
                now_child.f = now_child.g + now_child.h

                if len([openNode for openNode in openlist
                        if now_child == openNode and now_child.g > openNode.g]) > 0:
                       continue

                openlist.append(now_child)
                




    path = A_star()
     



    return path

    ############################################################################


# -------------------- Stage 02: Four circles - A* Algorithm  ------------------------ #



def stage2_heuristic(maze,p1,start,min_dis):
            
    return manhatten_dist(p1.location,start) + min_dis


def A_star_circle(maze,start_point,end_point):
        #초기화하기


        openlist = []
        closedlist=[]
        
        index = 0
      
        startN = Node(None,start_point)
        endN = Node(None,end_point)
        
        openlist.append(startN)
        while openlist:
           node = openlist[0]
           index = 0
           for i,j in enumerate(openlist):
               
               if j.f < node.f:
                   index = i
                   node = j
                  

          
           openlist.pop(index)
           closedlist.append(node)
          

           if node == endN:
             
                path = []
                now_N = node
                while now_N is not None:
                   path.append(now_N.location)
                
                   now_N = now_N.parent
                
                return len(path)


           child = []
        
           for i in maze.neighborPoints(node.location[0],node.location[1]):
         
                node_append = Node(node,i)
                child.append(node_append)
         
           for now_child in child:
          
                if now_child in closedlist:
          
                    continue
           
                now_child.g = node.g + 1
                now_child.h = manhatten_dist(now_child.location,endN.location)
                now_child.f = now_child.g + now_child.h

                if len([openNode for openNode in openlist
                        if now_child == openNode and now_child.g > openNode.g]) > 0:
                       continue

                openlist.append(now_child)
                
     






def astar_four_circles(maze):
    """
    [문제 03] 제시된 stage2의 맵 세가지를 A* Algorithm을 통해 최단 경로를 return하시오.(30점)
    (단 Heurstic Function은 위의 stage2_heuristic function을 직접 정의하여 사용해야 한다.)
    """
    
    
    end_points=maze.circlePoints()
    end_points.sort()

    path=[]

    ####################### Write Your Code Here ################################
    
    new_end_points = end_points
 
    dis = []
    a=0
    astar_dis_dict = dict()
    for i in range(0,len(new_end_points)):
        for j in range(i+1,len(new_end_points)):
            astar_dis_dict[new_end_points[i],new_end_points[j]] = A_star_circle(maze,new_end_points[i],new_end_points[j])
    
    copy_astar = astar_dis_dict.copy()
    for i in copy_astar:
        astar_dis_dict[i[1],i[0]] = astar_dis_dict[i]
    min_dis_index = (0,0),(1,1)
    min_dis_index2 = (0,0),(1,1)
    for k in astar_dis_dict:
       for j in astar_dis_dict:
           if (k[0]!=j[0]) and (k[0]!=j[1]) and k[1]!=j[0] and k[1]!=j[1]:
              
               result = astar_dis_dict[k] + astar_dis_dict[j]+astar_dis_dict[(k[1],j[0])]
               dis.append(result)
               if(result == min(dis)):
                   min_dis_index = k
                   min_dis_index2 = j
    
    start = min_dis_index[0]
    min_dis = min(dis)

    
    new_end_points = [min_dis_index[0],min_dis_index[1],min_dis_index2[0],min_dis_index2[1]]
    new2_end_points = list(reversed(new_end_points))
    
    if(A_star_circle(maze,new_end_points[0],maze.startPoint())<A_star_circle(maze,new2_end_points[0],maze.startPoint())):
        pass
    else:
        new_end_points = new2_end_points
    
  
    start_point = maze.startPoint()
    def A_star(start_sub,end_sub,endNode_index):
        #초기화하기

        
        openlist = []
        closedlist=[]
        
        index = 0
      
        startN = Node(None,start_sub)
        endN = Node(None,end_sub)
       
        openlist.append(startN)
        #시작노드 추가
        
        while openlist:
           node = openlist[0]
           index = 0
           
           for i,j in enumerate(openlist):
              
               if j.f < node.f:
                   index = i
                   node = j
                 

          
           openlist.pop(index)
           closedlist.append(node)
          
          

           if node == endN:
                
                sub_path = []
                now_N = node
                while now_N is not None:
                   sub_path.append(now_N.location)
                  
                   now_N = now_N.parent
                return sub_path[::-1]


           child = []
          
           for i in maze.neighborPoints(node.location[0],node.location[1]):
            
                node_append = Node(node,i)
                child.append(node_append)
          
           for now_child in child:
             
                if now_child in closedlist:
                  
                    continue
                
                now_child.g = node.g + 1
             
                now_child.h = stage2_heuristic(maze,now_child,start,min_dis)
               
                now_child.f = now_child.g + now_child.h

                if len([openNode for openNode in openlist
                        if now_child == openNode and now_child.g > openNode.g]) > 0:
                       continue

                openlist.append(now_child)
                

    
    path1 = []
    path1 = (A_star(start_point,new_end_points[0],0))
    
    path1.pop()
    for i in range(len(end_points)-1):
        path1 = path1 + ( A_star(new_end_points[i],new_end_points[i+1],i+1))
        if i != len(end_points)-2:
            path1.pop()
  
        
    return path1

    ############################################################################



# -------------------- Stage 03: Many circles - A* Algorithm -------------------- #

def mst(objectives, edges):

    cost_sum=0
    ####################### Write Your Code Here ################################
    cost_list = []
    mstt = list()
    adj = defaultdict(list)
    start = objectives[0]
    # initialize list, start
    for a,b in edges:
        adj[a].append((edges[(a,b)],a,b))
        adj[b].append((edges[(a,b)],b,a))
                #인접하는 edge값 저장하
    connect = set([start])
    fringe = adj[start]
    heapify(fringe)
    #make heap from fringe
    temp=start
    k=0
    while fringe:
        w,a1,b1 = heappop(fringe)
                
        if (b1 not in connect) :
            connect.add(b1)
            mstt.append((w,a1,b1))
            cost_sum = cost_sum+w
            
            temp = b1
            for jj in adj[b1]:
                if jj[2] not in connect:
                    heappush(fringe,jj)
                       
    cost_list.append(0)
  

    return cost_sum,mstt

    ############################################################################

def stage3_heuristic(objectives,edges,now_child,start,maze,max_dis,node_list):
    
    cost_num,mstt = mst(objectives,edges)
    
    
    return cost_num - A_star_circle(maze,now_child,mstt[0][1]) + A_star_circle(maze,start,now_child) 

def astar_many_circles(maze):
    """
    [문제 04] 제시된 stage3의 맵 세가지를 A* Algorithm을 통해 최단 경로를 return하시오.(30점)
    (단 Heurstic Function은 위의 stage3_heuristic function을 직접 정의하여 사용해야 하고, minimum spanning tree
    알고리즘을 활용한 heuristic function이어야 한다.)
    """

    end_points= maze.circlePoints()
    end_points.sort()

    path1=[]
    path = []
    ####################### Write Your Code Here ################################



                


    edges = dict()
    
    for i in range(len(end_points)-1):
        edges[end_points[i],end_points[i+1]] = A_star_circle(maze,end_points[i],end_points[i+1])
  
    end_num=0
    node_list = []

    start_point = maze.startPoint()
    node_list.append(start_point)
    def A_star(start_sub,node_list):
        #초기화하기
        openlist = []
        closedlist=[]
        mst_list = []
        path = []
        index = 0
        end_num=0
        startN = Node(None,start_sub)
        openlist.append(startN)
        max_dis = 0
        max_locat=0
        while openlist:
           node = openlist[0]
           index = 0
           for i,j in enumerate(openlist):
               if j.f < node.f:
                   index = i
                   node = j
                 
           openlist.pop(index)
           closedlist.append(node)
           closed_to_mst = []
           for i in closedlist:
                closed_to_mst.append(i.location)
        

           if node.location in end_points:
                end_num = end_num + 1
       
                

           child = []
           for i in maze.neighborPoints(node.location[0],node.location[1]):
                node_append = Node(node,i)
                child.append(node_append)
           for now_child in child:
                if now_child in closedlist:
                    continue
                
                
                now_child.g = node.g + 1
                closed_to_mst = []
                for i in closedlist:
                    closed_to_mst.append(i.location)
                mst_list = list(set(end_points) -set(node_list))
                edges2 = dict()
            
                
                now_child.h = stage3_heuristic(mst_list,edges,now_child.location,startN.location,maze,max_locat,node_list[-1])
               
                now_child.f = now_child.g + now_child.h
                
                if len([openNode for openNode in openlist
                        if now_child == openNode and now_child.g > openNode.g]) > 0:
                       continue

                openlist.append(now_child)
            
           if node.location in end_points and node.location not in node_list:
                
                sub_path = []
                now_N = node
                while now_N is not None:
                   sub_path.append(now_N.location)
                   
                   now_N = now_N.parent
                node_list.append(node.location)
                return sub_path[::-1],node

    
    path1 = []
    path2 = []
    path1,node = (A_star(start_point,node_list))
    path1.pop()

    for i in range(len(end_points)-1):
        
        path2, node1 = A_star(node.location,node_list)
        if(i != len(end_points)-2):
            path2.pop()
        path1 = path1+path2
        node = node1
  

    return path1



    ############################################################################



