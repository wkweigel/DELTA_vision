### <>This code evaluates a single string in DEL topology notation.
### <>The string is deconvoluted into a list of discrete topological elements.
### <>The list is then evalutated for connectivity between these elements.
### <>The output includes a list of individual elements, the detected connections, 
###   an adjacency list, an adjacency matrix, an edge list, and a final html file 
###   with and interactive network graph of the topological input.

#### <><><>BUGNOTES<><><>
# <>No detected connection for branched cyclic elements that fall at the end of the list.
#   the code for handling this just needs to written.  

#Imports modules
from turtle import color
import networkx as nx
import matplotlib.pylab as plt
import numpy as np
from pyvis.network import Network


top_strings=['AB','ABC','!ABCD!', 'A!BCD!', 'ABCDE', 'AB(C)DE', 'A!BC(D!)E' ,'ABCD','AB(C)D', '!ABC!D']
elements = 'ABCDEFGHIJKLMNOP'
linkers = "abcdefgh"
elements_list= list(elements)
linkers_list= list(linkers)

top_list=[]



def process_topology(topology):
    global elements 
    global linkers 
    global elements_list
    global linkers_list
    global top_list
    global add_edge
    global make_edge_list
    global print_graph
    global vertices
    global edge_list
    global vertices_no
    global graph

    branch_element=False
    cycle_element=False
    cycle_check=False
    branchcycle_start=False
    endsearch=False
 
    for idx, char in enumerate(topology):
        #Adds branching cyclic elements
        if branchcycle_start is True:
            top_list.append("(!" + char + ")")
            branchcycle_start=False
            branch_element=False
            endsearch=True
            continue
        #Adds branching elements
        if branch_element is True:
            if char == '!':
                branchcycle_start=True
                continue
            else: 
                top_list.append("(" + char + ")")
                branch_char=char
                cycle_check=True
                branch_element=False
                continue
        #Adds cyclic elements
        if cycle_element is True and endsearch is False:
            top_list.append("!" + char)
            endsearch=True
            cycle_element=False
            continue
        elif cycle_element is True and endsearch is True:
            top_list[-1]=last_element+"!"
            endsearch=False
            cycle_element=False
            continue
        #Adds normal elements
        if char in elements_list: 
            top_list.append(char)
        #Adds linker elements 
        elif char in linkers_list:
            top_list.append(char)
        #Detects branch elements
        elif char == '(':
            branch_element=True
        elif char == ')':
            continue
        #Detects cyclic elements
        elif char =='!':
            cycle_element=True
            if cycle_element is True and cycle_check is True:
                top_list[-1]="("+branch_char+"!)"
                cycle_check=False
                cycle_element=False
                continue
            if cycle_element is True and endsearch is True:
                top_list[-1]=last_element+"!"
                endsearch=False
                cycle_element=False
                continue
            if idx==0:
                continue
        last_element=top_list[-1]


    top_list.append("DNA")



    # Add vertices to the graph
    for i in top_list:
        add_vertex(i)

    #Adds edges to elements in top_list
    C1 = False
    C2 = False
    B_C1=False
    B_C2=False
    for A in top_list:
        bonds=1
        connections=0
        A_index=top_list.index(A)
        #Parses branched cyclic elements
        if A =='DNA':
            if '(' in top_list[-2]:
                DNA_connection=top_list[-3]
            else:
                DNA_connection=top_list[-2]
                add_edge(DNA_connection, A, 1)
            continue
        
        
        if '(' in A and '!' in A:
            cycle_list=list(A)
            for cycle_point in A:
                if cycle_list[1] == '!':
                    Br_cycle_start=A
                    B_C1=True
                    break
                if cycle_list[2] == '!':
                    Br_cycle_end=A
                    B_C2=True
                    break

        #Parses branched elements and adds edges
        if '(' in A:
            for B in top_list:
                B_index=top_list.index(B)
                if B_index<A_index:
                    continue
                if bonds <= connections: 
                    break
                if A == B:
                    add_edge(A, A, 0)
                if B_index==A_index:
                    add_edge(A, top_list[B_index-1], 1)
                    connections=connections+1
                    break

        #Parses cyclic elements
        if '!' in A:
            if '(' in A:
                continue
            else:
                cycle_list=list(A)
                for cycle_point in A:
                    if cycle_list[0] == '!':
                        cycle_start=A
                        C1=True
                        break
                    if cycle_list[1] == '!':
                        cycle_end=A
                        C2=True
                        break

        #Adds edges between normal cyclic elements
        if C1 and C2 == True:
            add_edge(cycle_start, cycle_end, 1)
            C1 = False
            C2 = False

        #Handles the addition of edges between various cases of branches cyclic elements
        if C1 and B_C2 == True:
            add_edge(cycle_start, Br_cycle_end, 1)
            C1 = False
            B_C2 = False
        
        if B_C1 and C2 == True:
            add_edge(Br_cycle_start, cycle_end, 1)
            B_C1 = False
            C2 = False
        
        if B_C1 and B_C2 == True:
            add_edge(Br_cycle_start, Br_cycle_end, 1)
            B_C1 = False
            B_C2 = False

        #Adds edges involving normal elements
        for B in top_list:
            B_index=top_list.index(B)
            if B=='DNA':
                break
            if B_index<A_index:
                continue
            if bonds <= connections: 
                break
            if A == B:
                add_edge(A, A, 0) 
            elif '(' in B:
                if '!' in B:
                    continue
                else:
                    add_edge(A, B, 1)
                    add_edge(A, top_list[B_index+1], 1)
                    connections=connections+2
            elif B in elements_list or linkers_list:
                add_edge(A, B, 1)
                connections=connections+1
    make_edge_list()

    

    node_color=[]
    for element in top_list:
        if element == 'DNA':
            node_color.append('red')
        else:
            node_color.append('blue') 


    #Creates network graph file
    DEL= Network()

    DEL.add_nodes(top_list, color=node_color)

    DEL.add_edges(edge_list, )

    DEL.show(topology+".html")


def refresh_vars():

    global top_list
    global edge_list
    global vertices
    global vertices_no
    global graph
    
    top_list=[] 
    vertices=[]              
    vertices_no = 0
    graph = []
    edge_list=[]


### Add a vertex to the set of vertices and the graph
def add_vertex(v):
  global graph
  global vertices_no
  global vertices
  if v in vertices:
    #print("Vertex ", v, " already exists")
    pass
  else:
    vertices_no = vertices_no + 1
    vertices.append(v)
    if vertices_no > 1:
        for vertex in graph:
            vertex.append(0)
    temp = []
    for i in range(vertices_no):
        temp.append(0)
    graph.append(temp)

# Add an edge between vertex v1 and v2 with edge weight e
def add_edge(v1, v2, e):
    global graph
    global vertices_no
    global vertices
    if v1 not in vertices:
        pass
        #print("Vertex ", v1, " does not exist.")
    elif v2 not in vertices:
        pass
        #print("Vertex ", v2, " does not exist.")
    else:
        index1 = vertices.index(v1)
        index2 = vertices.index(v2)
        graph[index1][index2] = e

# Print the graph
def print_graph():
  global graph
  global vertices_no
  for i in range(vertices_no):
    for j in range(vertices_no):
      if graph[i][j] != 0:
        print(vertices[i], " -> ", vertices[j], \
        "reaction ID: ", graph[i][j])

# make edge list
def make_edge_list():
  global graph
  global vertices_no
  for i in range(vertices_no):
    for j in range(vertices_no):
      if graph[i][j] != 0:
        X=vertices[i]
        Y=vertices[j]
        edge_list.append([X,Y])



#Prints all 
def print_all(): 
    #Prints list of elements
    print ("Individual Elements:")
    print(top_list)
    print("")

    #Prints detected connections
    print("Detected Connections:")
    print_graph()
    print("")

    #Prints adjacency list
    print("List Representation: ")
    print(graph)
    print("")

    #Prints adjacency matrix
    print("Matrix Representation: ")
    for line in graph:
        print(line)
    print("")

    #Creates keyed dictionary for elements and connections
    D = dict(zip(top_list, graph))
    
    # Prints resultant dictionary 
    print ("Dictionary Representation:" )
    print(str(D))
    print("")

    #Prints edge list
    print("Edge List:")
    print(edge_list)





# stores the vertices in the graph
vertices = []

# stores the number of vertices in the graph
vertices_no = 0
graph = []

#Stores edge list values
edge_list=[]




