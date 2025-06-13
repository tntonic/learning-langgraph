"""
Company Research System - Advanced LangGraph Implementation
This system researches companies by coordinating multiple specialized agents
to gather and analyze data from various sources.
"""

import os
from typing import TypedDict, Literal, List, Dict, Any, Annotated
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from datetime import datetime
import json
import operator
from IPython.display import Image, display

# Initialize LLM (you can also use local models)
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# Define the state that flows between agents
class CompanyResearchState(TypedDict):
    company_name: str
    ticker: str
    research_objective: str
    
    # Financial data
    financial_metrics: Dict[str, Any]
    revenue_trends: List[Dict]
    profitability_analysis: str
    
    # Market position
    market_share: float
    competitors: List[str]
    competitive_advantages: List[str]
    competitive_risks: List[str]
    
    # News and sentiment
    recent_news: List[Dict]
    sentiment_score: float
    key_events: List[str]
    
    # Leadership and culture
    leadership_info: Dict[str, Any]
    company_culture: str
    employee_sentiment: float
    
    # Technology and innovation
    tech_stack: List[str]
    patents: List[str]
    rd_investments: float
    
    # ESG and risks
    esg_score: Dict[str, float]
    risk_factors: List[str]
    regulatory_issues: List[str]
    
    # Final outputs
    investment_recommendation: str
    executive_summary: str
    detailed_report: str
    confidence_score: float
    
    # Workflow management
    messages: Annotated[List, operator.add]
    errors: List[str]
    data_sources: List[str]
    research_depth: Literal["quick", "standard", "deep"]

# Define specialized agent nodes

def company_identifier(state: CompanyResearchState) -> CompanyResearchState:
    """Identifies and validates the company, gets basic info"""
    print(f"🏢 Company Identifier: Researching {state['company_name']}...")
    
    # Simulate company identification
    # In production, this would call APIs like Yahoo Finance, Bloomberg, etc.
    
    prompt = f"""
    For the company "{state['company_name']}", provide:
    1. Official company name
    2. Stock ticker symbol (if public)
    3. Industry classification
    4. Headquarters location
    5. Year founded
    
    Format as JSON.
    """
    
    # Simulate response
    state['ticker'] = state.get('ticker', 'PRIVATE')
    state['data_sources'].append('Company Database')
    state['messages'].append(AIMessage(content=f"Identified company: {state['company_name']}"))
    
    return state

def financial_analyst(state: CompanyResearchState) -> CompanyResearchState:
    """Analyzes financial metrics and performance"""
    print("💰 Financial Analyst: Analyzing financial data...")
    
    # Simulate financial analysis
    # In production, integrate with financial APIs (Alpha Vantage, IEX Cloud, etc.)
    
    state['financial_metrics'] = {
        'revenue': 1000000000,
        'revenue_growth': 0.15,
        'profit_margin': 0.20,
        'debt_to_equity': 0.5,
        'current_ratio': 1.8,
        'pe_ratio': 25.5
    }
    
    state['revenue_trends'] = [
        {'year': 2021, 'revenue': 800000000},
        {'year': 2022, 'revenue': 900000000},
        {'year': 2023, 'revenue': 1000000000}
    ]
    
    state['profitability_analysis'] = "Strong profit margins with consistent growth"
    state['data_sources'].append('Financial APIs')
    state['messages'].append(AIMessage(content="Financial analysis completed"))
    
    return state

def market_analyst(state: CompanyResearchState) -> CompanyResearchState:
    """Analyzes market position and competition"""
    print("📊 Market Analyst: Evaluating market position...")
    
    # Simulate competitive analysis
    # In production, use industry databases, web scraping, etc.
    
    prompt = f"""
    Analyze the competitive landscape for {state['company_name']}:
    1. Main competitors
    2. Market share estimate
    3. Competitive advantages
    4. Competitive threats
    """
    
    state['competitors'] = ['Competitor A', 'Competitor B', 'Competitor C']
    state['market_share'] = 0.25
    state['competitive_advantages'] = [
        'Strong brand recognition',
        'Superior technology platform',
        'Extensive distribution network'
    ]
    state['competitive_risks'] = [
        'New market entrants',
        'Price competition',
        'Technology disruption'
    ]
    
    state['data_sources'].append('Industry Reports')
    state['messages'].append(AIMessage(content="Market analysis completed"))
    
    return state

def news_sentiment_analyst(state: CompanyResearchState) -> CompanyResearchState:
    """Analyzes recent news and market sentiment"""
    print("📰 News Analyst: Tracking news and sentiment...")
    
    # Simulate news analysis
    # In production, use news APIs (NewsAPI, Benzinga, etc.)
    
    state['recent_news'] = [
        {
            'date': '2024-01-15',
            'headline': f'{state["company_name"]} Announces Record Q4 Earnings',
            'sentiment': 'positive',
            'impact': 'high'
        },
        {
            'date': '2024-01-10',
            'headline': f'{state["company_name"]} Launches New AI Product Line',
            'sentiment': 'positive',
            'impact': 'medium'
        }
    ]
    
    state['sentiment_score'] = 0.75  # 0-1 scale
    state['key_events'] = [
        'Q4 earnings beat expectations',
        'New product launch successful',
        'Strategic partnership announced'
    ]
    
    state['data_sources'].append('News APIs')
    state['messages'].append(AIMessage(content="News sentiment analysis completed"))
    
    return state

def leadership_culture_analyst(state: CompanyResearchState) -> CompanyResearchState:
    """Analyzes leadership team and company culture"""
    print("👥 Leadership Analyst: Evaluating management and culture...")
    
    # Simulate leadership analysis
    # In production, use LinkedIn API, Glassdoor, etc.
    
    state['leadership_info'] = {
        'ceo_tenure': 5,
        'management_stability': 'high',
        'board_independence': 0.8,
        'insider_ownership': 0.15
    }
    
    state['company_culture'] = 'Innovation-focused with strong employee engagement'
    state['employee_sentiment'] = 0.82  # Based on review sites
    
    state['data_sources'].append('Professional Networks')
    state['messages'].append(AIMessage(content="Leadership analysis completed"))
    
    return state

def technology_innovation_analyst(state: CompanyResearchState) -> CompanyResearchState:
    """Analyzes technology stack and innovation capacity"""
    print("🔬 Tech Analyst: Assessing technology and innovation...")
    
    # Simulate tech analysis
    # In production, analyze job postings, patents, tech blogs
    
    state['tech_stack'] = ['Cloud-native', 'AI/ML', 'Microservices', 'DevOps']
    state['patents'] = ['AI-based recommendation system', 'Distributed computing method']
    state['rd_investments'] = 0.15  # As percentage of revenue
    
    state['data_sources'].append('Patent Databases')
    state['messages'].append(AIMessage(content="Technology analysis completed"))
    
    return state

def esg_risk_analyst(state: CompanyResearchState) -> CompanyResearchState:
    """Analyzes ESG factors and risk profile"""
    print("🌍 ESG Analyst: Evaluating sustainability and risks...")
    
    # Simulate ESG analysis
    # In production, use ESG data providers (MSCI, Sustainalytics)
    
    state['esg_score'] = {
        'environmental': 0.75,
        'social': 0.80,
        'governance': 0.85
    }
    
    state['risk_factors'] = [
        'Regulatory changes in key markets',
        'Supply chain dependencies',
        'Cybersecurity threats'
    ]
    
    state['regulatory_issues'] = ['Data privacy compliance', 'Environmental regulations']
    
    state['data_sources'].append('ESG Databases')
    state['messages'].append(AIMessage(content="ESG analysis completed"))
    
    return state

def report_synthesizer(state: CompanyResearchState) -> CompanyResearchState:
    """Synthesizes all research into comprehensive report"""
    print("📝 Report Synthesizer: Creating comprehensive analysis...")
    
    # Calculate confidence score based on data completeness
    data_points = [
        state.get('financial_metrics'),
        state.get('competitors'),
        state.get('recent_news'),
        state.get('leadership_info'),
        state.get('esg_score')
    ]
    state['confidence_score'] = sum(1 for dp in data_points if dp) / len(data_points)
    
    # Generate executive summary
    state['executive_summary'] = f"""
    EXECUTIVE SUMMARY - {state['company_name']}
    
    Financial Performance: {state.get('profitability_analysis', 'Analysis pending')}
    Market Position: {state.get('market_share', 0)*100:.1f}% market share
    Sentiment Score: {state.get('sentiment_score', 0)*100:.0f}% positive
    ESG Rating: {sum(state.get('esg_score', {}).values())/3*100:.0f}/100
    
    Key Strengths:
    {chr(10).join(f'• {adv}' for adv in state.get('competitive_advantages', [])[:3])}
    
    Key Risks:
    {chr(10).join(f'• {risk}' for risk in state.get('risk_factors', [])[:3])}
    
    Research Confidence: {state['confidence_score']*100:.0f}%
    """
    
    # Generate investment recommendation
    score = (
        state.get('sentiment_score', 0.5) * 0.3 +
        (state.get('financial_metrics', {}).get('revenue_growth', 0) > 0.1) * 0.3 +
        (sum(state.get('esg_score', {}).values()) / 3) * 0.2 +
        (state.get('employee_sentiment', 0.5)) * 0.2
    )
    
    if score > 0.7:
        state['investment_recommendation'] = "STRONG BUY"
    elif score > 0.6:
        state['investment_recommendation'] = "BUY"
    elif score > 0.4:
        state['investment_recommendation'] = "HOLD"
    else:
        state['investment_recommendation'] = "SELL"
    
    state['messages'].append(AIMessage(content="Research synthesis completed"))
    
    return state

def quality_validator(state: CompanyResearchState) -> CompanyResearchState:
    """Validates research quality and completeness"""
    print("✅ Quality Validator: Checking research completeness...")
    
    # Check for missing critical data
    critical_fields = ['financial_metrics', 'competitors', 'risk_factors']
    missing = [field for field in critical_fields if not state.get(field)]
    
    if missing:
        state['errors'].append(f"Missing critical data: {', '.join(missing)}")
    
    # Validate data freshness (in production, check timestamps)
    state['messages'].append(AIMessage(content=f"Quality validation completed. Confidence: {state['confidence_score']*100:.0f}%"))
    
    return state

# Define routing logic
def determine_research_depth(state: CompanyResearchState) -> str:
    """Routes to different analysis paths based on research depth"""
    depth = state.get('research_depth', 'standard')
    
    if depth == 'quick':
        return 'quick_analysis'
    elif depth == 'deep':
        return 'deep_analysis'
    else:
        return 'standard_analysis'

def should_enhance_research(state: CompanyResearchState) -> Literal["enhance", "complete"]:
    """Determines if additional research is needed"""
    if state['confidence_score'] < 0.7 and len(state['errors']) == 0:
        return "enhance"
    return "complete"

# Build the graph
def create_company_research_graph():
    builder = StateGraph(CompanyResearchState)
    
    # Add all nodes
    builder.add_node("company_identifier", company_identifier)
    builder.add_node("financial_analyst", financial_analyst)
    builder.add_node("market_analyst", market_analyst)
    builder.add_node("news_sentiment_analyst", news_sentiment_analyst)
    builder.add_node("leadership_culture_analyst", leadership_culture_analyst)
    builder.add_node("technology_innovation_analyst", technology_innovation_analyst)
    builder.add_node("esg_risk_analyst", esg_risk_analyst)
    builder.add_node("report_synthesizer", report_synthesizer)
    builder.add_node("quality_validator", quality_validator)
    
    # Define the flow
    builder.add_edge(START, "company_identifier")
    
    # Parallel analysis paths
    builder.add_edge("company_identifier", "financial_analyst")
    builder.add_edge("company_identifier", "market_analyst")
    builder.add_edge("company_identifier", "news_sentiment_analyst")
    
    # Standard flow includes these
    builder.add_edge("financial_analyst", "leadership_culture_analyst")
    builder.add_edge("market_analyst", "technology_innovation_analyst")
    builder.add_edge("news_sentiment_analyst", "esg_risk_analyst")
    
    # All paths converge at synthesis
    builder.add_edge("leadership_culture_analyst", "report_synthesizer")
    builder.add_edge("technology_innovation_analyst", "report_synthesizer")
    builder.add_edge("esg_risk_analyst", "report_synthesizer")
    
    # Quality check
    builder.add_edge("report_synthesizer", "quality_validator")
    
    # Conditional ending
    builder.add_conditional_edges(
        "quality_validator",
        should_enhance_research,
        {
            "enhance": "market_analyst",  # Loop back for more research
            "complete": END
        }
    )
    
    return builder.compile()

# Example usage and demonstration
if __name__ == "__main__":
    # Create the research graph
    graph = create_company_research_graph()
    
    # Save visualization
    try:
        img = Image(graph.get_graph().draw_mermaid_png())
        with open("company_research_graph.png", "wb") as f:
            f.write(img.data)
        print("📊 Graph visualization saved as company_research_graph.png")
    except Exception as e:
        print(f"Visualization error: {e}")
    
    # Print Mermaid diagram
    print("\n🎨 Mermaid Diagram:")
    print(graph.get_graph().draw_mermaid())
    
    # Run example research
    print("\n" + "="*60)
    print("🔍 COMPANY RESEARCH SYSTEM DEMO")
    print("="*60)
    
    # Test companies
    test_companies = [
        {"name": "Apple Inc.", "objective": "Investment analysis", "depth": "deep"},
        {"name": "Tesla", "objective": "Competitive positioning", "depth": "standard"},
        {"name": "Local Startup XYZ", "objective": "Acquisition target", "depth": "quick"}
    ]
    
    for company_info in test_companies[:1]:  # Run first example
        print(f"\n🏢 Researching: {company_info['name']}")
        print(f"📋 Objective: {company_info['objective']}")
        print(f"🔍 Research Depth: {company_info['depth']}")
        print("-" * 50)
        
        initial_state = {
            "company_name": company_info['name'],
            "ticker": "",
            "research_objective": company_info['objective'],
            "research_depth": company_info['depth'],
            "financial_metrics": {},
            "revenue_trends": [],
            "profitability_analysis": "",
            "market_share": 0.0,
            "competitors": [],
            "competitive_advantages": [],
            "competitive_risks": [],
            "recent_news": [],
            "sentiment_score": 0.0,
            "key_events": [],
            "leadership_info": {},
            "company_culture": "",
            "employee_sentiment": 0.0,
            "tech_stack": [],
            "patents": [],
            "rd_investments": 0.0,
            "esg_score": {},
            "risk_factors": [],
            "regulatory_issues": [],
            "investment_recommendation": "",
            "executive_summary": "",
            "detailed_report": "",
            "confidence_score": 0.0,
            "messages": [],
            "errors": [],
            "data_sources": []
        }
        
        try:
            # Run the research
            result = graph.invoke(initial_state)
            
            # Display results
            print(f"\n📊 RESEARCH RESULTS")
            print("="*50)
            print(result['executive_summary'])
            print(f"\n💡 Investment Recommendation: {result['investment_recommendation']}")
            print(f"\n📚 Data Sources Used: {', '.join(set(result['data_sources']))}")
            print(f"\n🔄 Research Steps:")
            for msg in result['messages']:
                print(f"  • {msg.content}")
                
        except Exception as e:
            print(f"Error: {e}")
            print("Note: This demo simulates data. In production, connect real data sources.")