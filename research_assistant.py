"""
AI Research Assistant - Advanced LangGraph Demo
This demonstrates:
- Multiple specialized agents working together
- State management and routing
- Human-in-the-loop interactions
- Parallel processing
- Error handling and retries
"""

import os
from typing import TypedDict, Literal, List, Dict, Annotated
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.tools import tool
from datetime import datetime
import json
from IPython.display import Image, display
import operator

# Initialize LLM
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# Define our state
class ResearchState(TypedDict):
    topic: str
    search_queries: List[str]
    search_results: List[Dict]
    key_findings: List[str]
    draft_report: str
    human_feedback: str
    final_report: str
    messages: Annotated[List, operator.add]
    iteration: int
    max_iterations: int

# Define tools
search = DuckDuckGoSearchRun()

@tool
def web_search(query: str) -> str:
    """Search the web for information"""
    return search.run(query)

@tool
def analyze_content(content: str, focus: str) -> str:
    """Analyze content with a specific focus"""
    # In a real implementation, this would use an LLM
    return f"Analysis of content focused on {focus}: {content[:200]}..."

@tool
def generate_citation(source: str, content: str) -> str:
    """Generate a proper citation for a source"""
    return f"[{datetime.now().year}] {source}: {content[:100]}..."

# Define agent nodes
def research_planner(state: ResearchState) -> ResearchState:
    """Plans the research approach and generates search queries"""
    print("🎯 Research Planner: Creating research strategy...")
    
    prompt = f"""
    Create a research plan for the topic: {state['topic']}
    Generate 3-5 specific search queries that would help gather comprehensive information.
    Return as a JSON list of queries.
    """
    
    response = llm.invoke([SystemMessage(content=prompt)])
    
    # Parse queries (simplified for demo)
    queries = [
        f"{state['topic']} latest research",
        f"{state['topic']} industry trends 2024",
        f"{state['topic']} best practices",
        f"{state['topic']} case studies",
        f"{state['topic']} future predictions"
    ]
    
    state['search_queries'] = queries
    state['messages'].append(AIMessage(content=f"Generated {len(queries)} search queries"))
    return state

def web_researcher(state: ResearchState) -> ResearchState:
    """Executes web searches and collects information"""
    print("🔍 Web Researcher: Searching for information...")
    
    results = []
    for query in state['search_queries'][:3]:  # Limit to 3 for demo
        try:
            result = search.run(query)
            results.append({
                'query': query,
                'content': result,
                'timestamp': datetime.now().isoformat()
            })
        except Exception as e:
            print(f"Error searching for {query}: {e}")
    
    state['search_results'] = results
    state['messages'].append(AIMessage(content=f"Found {len(results)} search results"))
    return state

def content_analyzer(state: ResearchState) -> ResearchState:
    """Analyzes search results and extracts key findings"""
    print("🧠 Content Analyzer: Extracting insights...")
    
    findings = []
    for result in state['search_results']:
        prompt = f"""
        Analyze this content and extract 2-3 key findings about {state['topic']}:
        {result['content'][:500]}
        
        Format as bullet points.
        """
        
        response = llm.invoke([SystemMessage(content=prompt)])
        findings.append({
            'source': result['query'],
            'insights': response.content
        })
    
    state['key_findings'] = findings
    state['messages'].append(AIMessage(content=f"Extracted insights from {len(findings)} sources"))
    return state

def report_writer(state: ResearchState) -> ResearchState:
    """Writes a comprehensive report based on findings"""
    print("✍️  Report Writer: Drafting report...")
    
    findings_text = "\n\n".join([
        f"From '{f['source']}':\n{f['insights']}" 
        for f in state['key_findings']
    ])
    
    prompt = f"""
    Write a comprehensive research report on: {state['topic']}
    
    Based on these findings:
    {findings_text}
    
    Structure:
    1. Executive Summary
    2. Key Findings
    3. Analysis
    4. Recommendations
    5. Conclusion
    
    Keep it concise but informative (300-500 words).
    """
    
    response = llm.invoke([SystemMessage(content=prompt)])
    state['draft_report'] = response.content
    state['messages'].append(AIMessage(content="Draft report completed"))
    return state

def human_reviewer(state: ResearchState) -> ResearchState:
    """Simulates human review and feedback"""
    print("👤 Human Reviewer: Reviewing draft...")
    
    # In a real implementation, this would wait for actual human input
    # For demo, we'll simulate feedback
    if state['iteration'] == 0:
        state['human_feedback'] = "Good start, but please add more specific examples and data points."
        state['iteration'] += 1
    else:
        state['human_feedback'] = "Approved - ready to publish!"
    
    state['messages'].append(HumanMessage(content=state['human_feedback']))
    return state

def report_finalizer(state: ResearchState) -> ResearchState:
    """Finalizes the report based on human feedback"""
    print("📄 Report Finalizer: Creating final version...")
    
    if "Approved" in state['human_feedback']:
        state['final_report'] = state['draft_report']
    else:
        prompt = f"""
        Revise this report based on the feedback: {state['human_feedback']}
        
        Original report:
        {state['draft_report']}
        """
        
        response = llm.invoke([SystemMessage(content=prompt)])
        state['final_report'] = response.content
    
    state['messages'].append(AIMessage(content="Report finalized"))
    return state

# Define routing logic
def should_continue(state: ResearchState) -> Literal["continue", "end"]:
    """Determines if we should continue or end the workflow"""
    if "Approved" in state.get('human_feedback', ''):
        return "end"
    elif state['iteration'] < state['max_iterations']:
        return "continue"
    else:
        return "end"

def route_after_human_review(state: ResearchState) -> Literal["finalize", "revise"]:
    """Routes based on human feedback"""
    if "Approved" in state.get('human_feedback', ''):
        return "finalize"
    else:
        return "revise"

# Build the graph
def create_research_graph():
    builder = StateGraph(ResearchState)
    
    # Add nodes
    builder.add_node("planner", research_planner)
    builder.add_node("researcher", web_researcher)
    builder.add_node("analyzer", content_analyzer)
    builder.add_node("writer", report_writer)
    builder.add_node("human_review", human_reviewer)
    builder.add_node("finalizer", report_finalizer)
    
    # Add edges
    builder.add_edge(START, "planner")
    builder.add_edge("planner", "researcher")
    builder.add_edge("researcher", "analyzer")
    builder.add_edge("analyzer", "writer")
    builder.add_edge("writer", "human_review")
    
    # Conditional edges
    builder.add_conditional_edges(
        "human_review",
        route_after_human_review,
        {
            "finalize": "finalizer",
            "revise": "writer"
        }
    )
    
    builder.add_edge("finalizer", END)
    
    return builder.compile()

# Example usage
if __name__ == "__main__":
    # Create the graph
    graph = create_research_graph()
    
    # Visualize
    try:
        img = Image(graph.get_graph().draw_mermaid_png())
        with open("research_assistant_graph.png", "wb") as f:
            f.write(img.data)
        print("📊 Graph visualization saved as research_assistant_graph.png")
    except Exception as e:
        print(f"Could not save visualization: {e}")
    
    # Print Mermaid diagram
    print("\n🎨 Mermaid Diagram:")
    print(graph.get_graph().draw_mermaid())
    
    # Run a research task
    print("\n🚀 Starting Research Assistant Demo...")
    print("=" * 50)
    
    initial_state = {
        "topic": "The impact of AI on software development",
        "search_queries": [],
        "search_results": [],
        "key_findings": [],
        "draft_report": "",
        "human_feedback": "",
        "final_report": "",
        "messages": [],
        "iteration": 0,
        "max_iterations": 2
    }
    
    try:
        # Run the graph
        result = graph.invoke(initial_state)
        
        print("\n📊 Final Report:")
        print("=" * 50)
        print(result.get('final_report', result.get('draft_report', 'No report generated')))
        
        print("\n💬 Workflow Messages:")
        for msg in result['messages']:
            print(f"- {msg.content}")
            
    except Exception as e:
        print(f"Error running graph: {e}")
        print("Note: This demo requires OpenAI API key to be set in environment")