# -*- coding: utf-8 -*-
"""
Created on Fri May 29 19:06:34 2020

@author: Bhau
"""

import random
input_data_file = open(r"gc_50_3","r")
input_data = input_data_file.read()
lines = input_data.split('\n')
firstLine = lines[0].split()                       
n_nodes = int(firstLine[0])
n_edges = int(firstLine[1])
edges=[]                                        # edges
All_possible_edges=[]                           # All edges  
color_node_matrix = {}                          # allocation of nodes to different colors key = color , values are nodes which we are assigning that color
New_color = 0                                   # numbering of color
Nodes_assigned_color = []                       # list of nodes who have assigned colors
nebhigours = {}                                 # key = node ,  Values = all connecting nodes to the key node
for i in range(n_edges):
    aa = lines[i+1].split()
    b = int(aa[0])
    c = int(aa[1])
    All_possible_edges.append((b,c))
    All_possible_edges.append((c,b))
    edges.append((b,c))                                
########## INput END #############
########## Data Preparation ######## Assigning nebhigours to node                       
for i in range(len(All_possible_edges)):
    if All_possible_edges[i][0] not in nebhigours:
        nebhigours[All_possible_edges[i][0]] = [All_possible_edges[i][1]]
    else:
        nebhigours[All_possible_edges[i][0]] = nebhigours[All_possible_edges[i][0]] + [All_possible_edges[i][1]]
##### Data Preparation End ############
# Match is function which finds that should we assigned New_Node in same color or not
# Match takes two input first is New_Node Second is set of nodes which having same color 
# New_Node = A node which we have to assign color       
def match(Nodes_of_color,New_Node):
    Nodes_of_color = set(Nodes_of_color)
    nebhigours_of_New_Node = set (nebhigours[New_Node])
    if list(Nodes_of_color.intersection(nebhigours_of_New_Node)) == []:
        return 'Not matched'
    else:
        return 'matched'
### First allocation of colors to nodes
copy_edges = edges[:]
for edge in edges:   
#    ran_num = random.randint(0,len(copy_edges)) 
#    edge = copy_edges[ran_num-1]
#    copy_edges.remove(edge)                               
    for node in edge:                                 
        if len(Nodes_assigned_color) == 0 :             ### for initiallisation i allocat two different colors to two nodes of first edge
            color_node_matrix[New_color] = [node]       ### first assignment of color to node
            New_color = New_color + 1
            Nodes_assigned_color.append(node)
        elif len(Nodes_assigned_color) <= n_nodes:      ### termination condition
            if node not in Nodes_assigned_color:        ## check for new nodes who has not assign color
                color_checked = []                      ## for assigning color to node we have to check that node whether we assign to colors at present or we have to add new color            
                for color in range(len(color_node_matrix)):
                    k = match(color_node_matrix[color],node)      
                    if k == 'Not matched':
                        color_node_matrix[color] = color_node_matrix[color] + [node]
                        Nodes_assigned_color.append(node)
                        break
                    else:
                        color_checked.append(color)
#### after checking for all colors if it is found new node has not allocated to any color
### we add new color
                if len(color_checked) == len(color_node_matrix):
                    color_node_matrix[New_color] = [node]
                    Nodes_assigned_color.append(node)
                    New_color = New_color + 1
### get first initial feasible solution
### in fun update_group we are shifting all nodes of colori to various other colorsj
### Shifting_node dict take care of shifting of nodes of colori to various colorj                     
def update_group(color_node_matrix):            
    for colori in range(len(color_node_matrix)):
        nodes_of_colori = color_node_matrix[colori]
        temp = nodes_of_colori[:]
        Node_shifting = {} ## for tracing shifting of nodes to different color if all nodes of colori shifts
        for node in nodes_of_colori:
            for colorj in color_node_matrix:
                if colori != colorj:  
                    if match(color_node_matrix[colorj],node) == 'Not matched':
                        temp.remove(node)
                        Node_shifting[node] = colorj       ###
                        if temp == []: ## if temp is empty it means we can delete colori and  
                                        # nodes of colori shift to various colorj according to Node_shifting dict
                            for node in Node_shifting :
                                alloted_new_color = Node_shifting[node]
                                color_node_matrix[alloted_new_color] = color_node_matrix[alloted_new_color] + [node]
                            color_node_matrix.pop(colori)
                        break
    ### for maintaing color sequence i have to revised names of color
    s = list(color_node_matrix.keys())
    qq = {}
    for i in range(len(color_node_matrix)):
        ss = s[i]
        qq[i] = color_node_matrix[ss]
    return qq
### shifting of node individually to other node groups 
def update_individual(color_node_matrix):            
    for colori in range(len(color_node_matrix)):
        nodes_of_colori = color_node_matrix[colori]
        for node in nodes_of_colori:
            for colorj in color_node_matrix:
                if colori != colorj:  
                    if match(color_node_matrix[colorj],node) == 'Not matched':
                        o = color_node_matrix[colori]
                        o.remove(node)
                        color_node_matrix[colori] = o
                        color_node_matrix[colorj] = color_node_matrix[colorj] + [node]
                        break
    return color_node_matrix
solution_50 = {}
solution_50['Initial'] = color_node_matrix
for i in range(50):
    color_node_matrix = update_group(color_node_matrix)
    color_node_matrix = update_individual(color_node_matrix)
    solution_50[i] = color_node_matrix

########## Tabu search #########
    
Tabu_color_node_matrix={}
Tabu_seq = {}
Tabu_color = []
iteration = 50
for n in range(iteration):
    all_present_colors= color_node_matrix.keys()
    non_tabu_color = set(all_present_colors) - set(Tabu_color)
    non_tabu_color = list(non_tabu_color)
    index= random.randint(0,len(non_tabu_color)-1)
    chosen_color = non_tabu_color[index]
    Nodes_of_chosen_color = color_node_matrix[chosen_color]
    shifted_nodes = []
    for node in Nodes_of_chosen_color:
        for color in color_node_matrix:
            if color != chosen_color:
                if color in Tabu_color:
#                    print(chosen_color,node,color, n)
                    if node not in Tabu_color_node_matrix[color]:
                        x = match(color_node_matrix[color],node)
                        if x == 'Not matched':
                            shifted_nodes.append(node)
                            o = color_node_matrix[chosen_color]
                            o.remove(node)
                            color_node_matrix[chosen_color] = o
                            color_node_matrix[color] = color_node_matrix[color] + [node]
                            break
                        else:
                            continue
                    else:
                        continue
                else:
                    x = match(color_node_matrix[color],node)
                    if x == 'Not matched':
                        shifted_nodes.append(node)
                        o = color_node_matrix[chosen_color]
                        o.remove(node)
                        color_node_matrix[chosen_color] = o
                        color_node_matrix[color] = color_node_matrix[color] + [node]
                        break
            else:
                continue
    if n < 3:
        Tabu_seq[n] = chosen_color
        Tabu_color_node_matrix[chosen_color] = shifted_nodes
        Tabu_color.append(chosen_color)
    else:
#        print('executed')
        seq = n%3
        color_remove = Tabu_seq[seq]
        Tabu_color_node_matrix.pop(color_remove)
        Tabu_color.remove(color_remove)
        Tabu_seq[seq] = chosen_color
        Tabu_color_node_matrix[chosen_color] = shifted_nodes
        Tabu_color.append(chosen_color)
#    print(Tabu_color_node_matrix , n , Tabu_color)
                    
                            
###### formating for Solution printing ########
global_solution = color_node_matrix
for n in solution_50:
    temp = solution_50[n]   
    if len(temp) < len(global_solution):
        global_solution = temp
ans = len(global_solution)
zz = []
for i in range(n_nodes):
    for j in global_solution:
        p = global_solution[j]
        if i in p:
            zz.append(j)
            break
output_data = str(ans) + ' ' + str(0) + '\n'
output_data += ' '.join(map(str, zz))
print(output_data)
