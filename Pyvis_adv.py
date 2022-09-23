# Import dependencies
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
#import networkx as nx
#from pyvis.network import Network
from DELTA import*


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
HtmlFile2 = open('G:/DEL Topology Tool (LAB)/Tree Generation/StreamLit Project/html_files/' + str(node_selection) + '.html','r',encoding='utf-8')
refresh_vars()

# Load HTML into HTML component for display on Streamlit

with st.expander("Node Inspector Window"):
    st.write("Select a node in the dropdown menu to view its topology")
    components.html(HtmlFile2.read(), width=800, height=800)

components.html(HtmlFile1.read(), width=800, height=800)




