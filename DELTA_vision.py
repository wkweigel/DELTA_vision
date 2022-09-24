# Import dependencies
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
#import networkx as nx
#from pyvis.network import Network
import networkx as nx
import matplotlib.pylab as plt
import numpy as np
from pyvis.network import Network



elements = 'ABCDEFGHIJKLMNOP'
linkers = "abcdefgh"
elements_list= list(elements)
linkers_list= list(linkers)

top_list=[]

# stores the vertices in the graph
vertices = []

# stores the number of vertices in the graph
vertices_no = 0
graph = []
graph_list={}

#Stores edge list values
edge_list=[]

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
    global HtmlFile2

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
    refresh_graph_info()
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

    

    node_colors=[]
    for element in top_list:
        if element == 'DNA':
            node_colors.append('#012A4A')
            continue
        for char in element:
            if char not in elements: 
                if char not in linkers and element != 'DNA':
                    continue
            else: 
                if 'A' in element:
                    node_colors.append('#A9D6E5')
                    break
                if 'B' in element:
                    node_colors.append('#61A5C2')
                    break
                if 'C' in element:
                    node_colors.append('#468FAF')
                    break
                if 'D' in element:
                    node_colors.append('#2A6F97')
                    break
                if 'E' in element:
                    node_colors.append('#014F86')
                    break
                if 'F' in element:
                    node_colors.append('#01497C')
                    break
                if 'G' in element:
                    node_colors.append('013A63')
                    break
                if 'H' in element:
                    node_colors.append('#013A63')
                    break
            if element in linkers and element != 'DNA': 
                node_colors.append('#FFE15C')


    node_shapes=[]
    for element in top_list:
        if element == 'DNA':
            node_shapes.append('dot')
        for char in element:
            if element=='DNA':
                continue
            if char in linkers:
                node_shapes.append('hexagon')
            if char in elements:
                node_shapes.append('dot')
            else:
                continue 

    
    #Creates network graph file
    DEL= Network()

    DEL.add_nodes(top_list, color=node_colors, shape=node_shapes)

    DEL.add_edges(edge_list)

    #DEL.show("del.html")

    # Save and read graph as HTML file (on Streamlit Sharing)
    try:
        path = '/tmp'
        DEL.save_graph(f'{path}/del.html')
        HtmlFile2 = open(f'{path}/del.html','r',encoding='utf-8')
    # Save and read graph as HTML file (locally)
    except:
        path = './'
        DEL.save_graph(f'{path}/del.html')
        HtmlFile2 = open(f'{path}/del.html','r',encoding='utf-8')


def refresh_graph_info():
    global edge_list
    global vertices
    global vertices_no
    global graph
    vertices=[]              
    vertices_no = 0
    graph = []
    edge_list=[]

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
#vertices = []

# stores the number of vertices in the graph
#vertices_no = 0
#graph = []

#Stores edge list values
#edge_list=[]



#<><><><><><><><><><><><><><><><><><><><><><><><><><><><><>


# Set header title
st.title('DEL Topology Visualization')


DEL_size= int(st.sidebar.selectbox('Number of diversity elements:',('3', '4', '5', '6', '7', '8')))

cycle_check = st.sidebar.radio('Consider cyclic topologies?',('Yes', 'No'), index=1)

lit_scale='No'

if cycle_check == 'Yes':
    lit_scale= st.sidebar.radio('Scale by literature prevalance?',('Yes', 'No'), index=1)

view= st.sidebar.radio ('Tree Layout:', ('Dendridic', 'Hierarchical'))



DE_string='ABCDEFGHIJK'
DE_selection=DE_string[:DEL_size]

sequence=DE_selection[1:]
seq_list=list(sequence)
nodes=['A']
growth_control={'A':'inactive', 'A':'active'}
branches=[['A', 'AB']]

temp_cyclic_string=''

global cyclic_list
cyclic_list=[]







def make_list(X, print_top_list=True):  
    global elements 
    global linkers 
    global elements_list
    global linkers_list
    global top_list
    global E_list
    global top_string
    global temp_cyclic_list

    top_list=[]
    E_list=[]
    C1_search=True
    C2_search=False
    char_behind=None
    char_ahead=None
    two_char_behind=None
    two_char_ahead=None
    char_list=list(X)

    top_string=X
    
    for idx, char in enumerate(X):
        #defines peek variables (characters before and after current idx value)
        if idx in range(1, len(char_list)):
            char_behind=char_list[idx-1]

        if idx in range(2, len(char_list)):
            two_char_behind=(char_list[idx-2])+(char_behind)

        if idx in range(0, len(char_list)-1):
            char_ahead=char_list[idx+1]

        if idx in range(0, len(char_list)-2):
            two_char_ahead=(char_ahead)+(char_list[idx+2])
            
        if char =='!':
            continue
        if char == '(' or char == ')':
            continue
        #Identifies the start of a branched-cyclic element
        if C1_search is True and two_char_behind =='(!':
            C1_search=False
            C2_search=True
            top_list.append('(!' + char + ')')
            continue
        #identifies the start of a cyclic element 
        elif C1_search is True and char_behind == '!':
            C1_search=False
            C2_search=True
            top_list.append('!' + char)
            continue
        #identifies the end of a branched-cyclic element
        elif C2_search is True and two_char_ahead =='!)':
            C2_search=False
            top_list.append('(' + char + '!)')
            continue
        #identifies the end of a cyclic element 
        elif C2_search is True and char_ahead =='!':
            C2_search=False
            top_list.append(char + '!')
            continue
        #identifies a branching element 
        elif char_behind =='(' and char_ahead == ')':
            top_list.append('(' + char + ')')
            continue

        elif char in linkers or char in elements:
            top_list.append(char)

    
    E_list.append(top_list)
    if print_top_list is True:
        print("Elements:")
        print(top_list)
        print("")
        


    # A,B,C,D -> !A,B,C!,D
    
        temp_cyclic_list=[]
    for IdxA, element in enumerate(top_list): #Outer for-loop controls all cyclic starting points
        temp_listA=top_list.copy()
        inital_end_point=IdxA+2
        if inital_end_point==len(top_list):
            break
        if len(top_list)<3:
            break
        if '(' in element:
            temp_listA[IdxA]="(!" + element[1] + ")"
        else:
            temp_listA[IdxA]="!" + element
        for IdxB in range(inital_end_point, len(top_list)):#Inner for-loop controls all cyclic ending points
            temp_listB=temp_listA.copy()
            temp_cycle=''
            if '(' in top_list[IdxB]: # For handling branch points, ie (X)
                for c in top_list[IdxB]:
                    if c == '(' or c == ')':
                        continue
                    else:
                        temp_listB[IdxB]="(" + c + "!)"
            else: # For handling regular elements
                temp_listB[IdxB]=top_list[IdxB] + "!" 
            for e in temp_listB:
                temp_cycle=temp_cycle + e
            temp_cyclic_list.append(temp_cycle)
            cyclic_list.append(temp_cycle)

def cyclic_tree_growth():
    make_list(key)
    for seq in temp_cyclic_list:
        nodes.append(seq)
        growth_control[seq]='inactive'
        branches.append([key,seq])






for letter in seq_list:
    for key,value in list(growth_control.items()):
        if value == 'active':
            new_node=str(key)+letter
            nodes.append(new_node)
            growth_control[new_node]='active'
            growth_control[key]='inactive'
            branches.append([key,new_node])
            if cycle_check == 'Yes':
                cyclic_tree_growth()
            

            if key == 'A':
                continue
            if key[-1]==')':
                if cycle_check == 'Yes':
                    cyclic_tree_growth()
                continue
            else:
                new_br_node=str(key) + '(' + letter + ')'
                nodes.append(new_br_node)
                growth_control[new_br_node]='active'
                branches.append([key,new_br_node])
                if cycle_check == 'Yes':
                    cyclic_tree_growth()
        if cycle_check == 'Yes':      
            for key,value in list(growth_control.items()):
                if value == 'active':
                    cyclic_tree_growth()
for i in nodes:
    add_vertex(i)

for X,Y in branches:
    add_edge(X,Y,1)

make_edge_list()


if lit_scale == 'Yes':
    df=pd.read_csv('G:\DEL Topology Tool (LAB)\Descriptor_Data.csv')

    temp_dict=df.set_index('Entry').to_dict()
    for k,v in temp_dict.items():
        occurance_dict=v



TREE= Network(height='800px',width='800px')

#TREE.add_nodes(nodes)

if lit_scale == 'No':
    for node in nodes:
        if '!' in node:
            TREE.add_node(node, shape="square", color="#fff9ae")
        else:
            TREE.add_node(node, shape="dot")

if lit_scale == 'Yes':
    for node in nodes:
        if node in occurance_dict.keys():
            if '!' in node:
                TREE.add_node(node, shape="square", color="#c6a8e0", size=occurance_dict.get(node)*10)
            else:
                TREE.add_node(node, shape="dot", color="#c6a8e0", size=occurance_dict.get(node)*10)
        elif '!' in node:
                TREE.add_node(node, shape="square", color="#fff9ae", size=10)
        else:
            TREE.add_node(node, shape="dot",size=10)

TREE.add_edges(edge_list)
#TREE.show_buttons()


if view=='Hierarchical':
    TREE.set_options("""
    const options = {
    "layout": {
        "hierarchical": {
        "enabled": true,
        "levelSeparation": 300,
        "nodeSpacing": 85,
        "treeSpacing": 150
        }
    },
    "physics": {
        "hierarchicalRepulsion": {
        "centralGravity": 0,
        "avoidOverlap": null
        },
        "minVelocity": 0.75,
        "solver": "hierarchicalRepulsion"
    }
    }
    """)


#TREE.show( 'Tree' + ".html")


# Save and read graph as HTML file (on Streamlit Sharing)
try:
   path = '/tmp'
   TREE.save_graph(f'{path}/Tree.html')
   HtmlFile1 = open(f'{path}/Tree.html','r',encoding='utf-8')
# Save and read graph as HTML file (locally)
except:
    path = './'
    TREE.save_graph(f'{path}/Tree.html')
    HtmlFile1 = open(f'{path}/Tree.html','r',encoding='utf-8')


#TREE.save_graph('Tree.html')
#HtmlFile1 = open('G:/DEL Topology Tool (LAB)/Tree Generation/StreamLit Project/Tree.html','r',encoding='utf-8')

#for node in nodes:
#    process_topology(node)

node_selection= st.sidebar.selectbox('Choose a node to inspect:',(nodes))
process_topology(str(node_selection))
#HtmlFile2 = open('G:/DEL Topology Tool (LAB)/Tree Generation/StreamLit Project/html_files/' + str(node_selection) + '.html','r',encoding='utf-8')
refresh_vars()
 
# Load HTML into HTML component for display on Streamlit

with st.expander("Node Inspector Window"):
    st.write("Select a node in the dropdown menu to view its topology")
    components.html(HtmlFile2.read(), width=800, height=800)

components.html(HtmlFile1.read(), width=800, height=800)




