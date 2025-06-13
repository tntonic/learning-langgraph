import random
from typing import Literal
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
import dotenv
dotenv.load_dotenv()

class State(TypedDict):
    graph_state: str

def node_1(state):
    print("---Node 1---")
    return {"graph_state": state['graph_state'] +" I am"}

def node_2(state):
    print("---Node 2---")
    return {"graph_state": state['graph_state'] +" happy!"}

def node_3(state):
    print("---Node 3---")
    return {"graph_state": state['graph_state'] +" sad!"}

def decide_mood(state) -> Literal["node_2", "node_3"]:
    if random.random() < 0.5:
        return "node_2"
    return "node_3"

# Build graph
builder = StateGraph(State)
builder.add_node("node_1", node_1)
builder.add_node("node_2", node_2)
builder.add_node("node_3", node_3)

# Logic
builder.add_edge(START, "node_1")
builder.add_conditional_edges("node_1", decide_mood)
builder.add_edge("node_2", END)
builder.add_edge("node_3", END)

# Compile
graph = builder.compile()

# Option 1: Save as PNG using Mermaid
try:
    from IPython.display import Image
    img = Image(graph.get_graph().draw_mermaid_png())
    with open("graph_visualization.png", "wb") as f:
        f.write(img.data)
    print("Graph saved as graph_visualization.png")
except Exception as e:
    print(f"Could not save as PNG: {e}")

# Option 2: Print Mermaid diagram text
print("\nMermaid diagram:")
print(graph.get_graph().draw_mermaid())

# Option 3: Save as DOT file for Graphviz
try:
    with open("graph.dot", "w") as f:
        f.write(graph.get_graph().draw_graphviz_dot())
    print("\nGraph saved as graph.dot (use Graphviz to render)")
except Exception as e:
    print(f"Could not save as DOT: {e}")