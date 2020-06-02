import random
input_data_file = open(r"gc_1000_5","r")
input_data = input_data_file.read()
lines = input_data.split('\n')
firstLine = lines[0].split()                       
n_nodes = int(firstLine[0])
n_edges = int(firstLine[1])
edges=[]                                        # edges
All_possible_edges=[]                           # All edges  
                          
New_color = 0                                   
Nodes_assigned_color = []                       
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
def feasibility_check(color_node_matrix):
    if sum(len(color_node_matrix[i]) for i in color_node_matrix) == n_nodes:
        return 'Solution is feasibli'
### First allocation of colors to nodes
solution_200 = {}
for n in range(1):
    New_color = 0   # numbering of color
    Nodes_assigned_color = [] # list of nodes who have assigned colors
    color_node_matrix = {}      # allocation of nodes to different colors key = color , values are nodes which we are assigning that color
    copy_edges = edges[:]
    for anyy in edges:   
        ran_num = random.randint(0,len(copy_edges)) 
        edge = copy_edges[ran_num-1]
        copy_edges.remove(edge)                               
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
    if feasibility_check(color_node_matrix) == 'Solution is feasibli':
        solution_200[n]= color_node_matrix
###### formating for Solution printing ########
global_solution = color_node_matrix
for n in solution_200:
    temp = solution_200[n]   
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
