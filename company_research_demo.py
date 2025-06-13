"""
Company Research System - LangGraph Demo (No API Required)
This demonstrates how LangGraph can orchestrate complex company research workflows
"""

from typing import TypedDict, Literal, List, Dict, Any, Annotated
from langgraph.graph import StateGraph, START, END
from datetime import datetime
import json
import operator
from IPython.display import Image, display
import random

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
    messages: Annotated[List[str], operator.add]
    errors: List[str]
    data_sources: List[str]
    research_depth: Literal["quick", "standard", "deep"]

# Simulate company data for demo
COMPANY_DATA = {
    "Apple Inc.": {
        "ticker": "AAPL",
        "industry": "Technology",
        "revenue": 385000000000,
        "employees": 164000,
        "founded": 1976,
        "competitors": ["Microsoft", "Google", "Samsung"],
        "market_cap": 3000000000000
    },
    "Tesla": {
        "ticker": "TSLA",
        "industry": "Automotive/Energy",
        "revenue": 96773000000,
        "employees": 127855,
        "founded": 2003,
        "competitors": ["BYD", "Volkswagen", "Ford"],
        "market_cap": 800000000000
    },
    "Amazon": {
        "ticker": "AMZN",
        "industry": "E-commerce/Cloud",
        "revenue": 574785000000,
        "employees": 1525000,
        "founded": 1994,
        "competitors": ["Microsoft", "Google", "Walmart"],
        "market_cap": 1700000000000
    }
}

# Define specialized agent nodes

def company_identifier(state: CompanyResearchState) -> CompanyResearchState:
    """Identifies and validates the company, gets basic info"""
    print(f"🏢 Company Identifier: Researching {state['company_name']}...")
    
    # Get company data if available
    company_info = COMPANY_DATA.get(state['company_name'], {})
    
    if company_info:
        state['ticker'] = company_info['ticker']
        state['messages'].append(f"✓ Identified {state['company_name']} (Ticker: {company_info['ticker']})")
        state['messages'].append(f"  Industry: {company_info['industry']}")
        state['messages'].append(f"  Founded: {company_info['founded']}")
    else:
        state['ticker'] = 'UNKNOWN'
        state['messages'].append(f"⚠️ Limited data available for {state['company_name']}")
    
    state['data_sources'].append('Company Database')
    return state

def financial_analyst(state: CompanyResearchState) -> CompanyResearchState:
    """Analyzes financial metrics and performance"""
    print("💰 Financial Analyst: Analyzing financial data...")
    
    company_info = COMPANY_DATA.get(state['company_name'], {})
    base_revenue = company_info.get('revenue', 1000000000)
    
    # Generate realistic financial metrics
    state['financial_metrics'] = {
        'revenue': base_revenue,
        'revenue_growth': round(random.uniform(0.05, 0.25), 2),
        'profit_margin': round(random.uniform(0.10, 0.30), 2),
        'debt_to_equity': round(random.uniform(0.3, 1.2), 2),
        'current_ratio': round(random.uniform(1.2, 2.5), 2),
        'pe_ratio': round(random.uniform(15, 35), 1),
        'market_cap': company_info.get('market_cap', base_revenue * 10)
    }
    
    # Generate revenue trends
    current_revenue = base_revenue
    state['revenue_trends'] = []
    for year in range(2021, 2024):
        growth = random.uniform(-0.05, 0.20)
        current_revenue = int(current_revenue * (1 + growth))
        state['revenue_trends'].append({
            'year': year,
            'revenue': current_revenue,
            'growth': round(growth * 100, 1)
        })
    
    # Analysis based on metrics
    if state['financial_metrics']['revenue_growth'] > 0.15:
        state['profitability_analysis'] = "Strong revenue growth with expanding margins"
    elif state['financial_metrics']['revenue_growth'] > 0.08:
        state['profitability_analysis'] = "Steady growth with stable profitability"
    else:
        state['profitability_analysis'] = "Moderate growth, focusing on efficiency"
    
    state['messages'].append(f"✓ Financial Analysis Complete:")
    state['messages'].append(f"  Revenue: ${base_revenue/1e9:.1f}B")
    state['messages'].append(f"  Growth Rate: {state['financial_metrics']['revenue_growth']*100:.0f}%")
    state['messages'].append(f"  P/E Ratio: {state['financial_metrics']['pe_ratio']}")
    
    state['data_sources'].append('Financial APIs')
    return state

def market_analyst(state: CompanyResearchState) -> CompanyResearchState:
    """Analyzes market position and competition"""
    print("📊 Market Analyst: Evaluating market position...")
    
    company_info = COMPANY_DATA.get(state['company_name'], {})
    
    # Get competitors
    state['competitors'] = company_info.get('competitors', ['Competitor A', 'Competitor B', 'Competitor C'])
    
    # Calculate market share based on company size
    if state['company_name'] in ["Apple Inc.", "Microsoft", "Amazon"]:
        state['market_share'] = round(random.uniform(0.20, 0.35), 2)
    else:
        state['market_share'] = round(random.uniform(0.05, 0.20), 2)
    
    # Generate competitive advantages based on company
    advantages_pool = {
        "Apple Inc.": [
            "Premium brand positioning",
            "Integrated ecosystem",
            "Strong customer loyalty",
            "Innovation in chip design"
        ],
        "Tesla": [
            "First-mover advantage in EVs",
            "Vertical integration",
            "Supercharger network",
            "Software and AI capabilities"
        ],
        "Amazon": [
            "Dominant e-commerce platform",
            "AWS cloud leadership",
            "Prime membership ecosystem",
            "Logistics infrastructure"
        ]
    }
    
    state['competitive_advantages'] = advantages_pool.get(
        state['company_name'], 
        ["Market leadership", "Strong brand", "Innovation capability"]
    )[:3]
    
    state['competitive_risks'] = [
        "Increasing competition",
        "Market saturation",
        "Regulatory pressures"
    ]
    
    state['messages'].append(f"✓ Market Analysis Complete:")
    state['messages'].append(f"  Market Share: {state['market_share']*100:.0f}%")
    state['messages'].append(f"  Main Competitors: {', '.join(state['competitors'][:2])}")
    
    state['data_sources'].append('Industry Reports')
    return state

def news_sentiment_analyst(state: CompanyResearchState) -> CompanyResearchState:
    """Analyzes recent news and market sentiment"""
    print("📰 News Analyst: Tracking news and sentiment...")
    
    # Generate realistic news based on company
    news_templates = {
        "positive": [
            f"{state['company_name']} Reports Record Quarterly Earnings",
            f"{state['company_name']} Launches Revolutionary New Product",
            f"{state['company_name']} Expands into New Markets"
        ],
        "neutral": [
            f"{state['company_name']} Announces Executive Changes",
            f"{state['company_name']} Updates Product Roadmap",
            f"{state['company_name']} Participates in Industry Conference"
        ],
        "negative": [
            f"{state['company_name']} Faces Supply Chain Challenges",
            f"{state['company_name']} Under Regulatory Scrutiny",
            f"{state['company_name']} Reports Lower Than Expected Growth"
        ]
    }
    
    # Generate mix of news
    state['recent_news'] = []
    sentiments = ['positive', 'positive', 'neutral', 'negative']  # Bias towards positive
    
    for i in range(3):
        sentiment = random.choice(sentiments)
        headline = random.choice(news_templates[sentiment])
        state['recent_news'].append({
            'date': f'2024-01-{15-i*5:02d}',
            'headline': headline,
            'sentiment': sentiment,
            'impact': 'high' if sentiment != 'neutral' else 'low'
        })
    
    # Calculate overall sentiment
    sentiment_values = {'positive': 1, 'neutral': 0.5, 'negative': 0}
    scores = [sentiment_values[news['sentiment']] for news in state['recent_news']]
    state['sentiment_score'] = sum(scores) / len(scores)
    
    state['key_events'] = [
        news['headline'].split(state['company_name'])[1].strip() 
        for news in state['recent_news'] 
        if news['sentiment'] == 'positive'
    ][:2]
    
    state['messages'].append(f"✓ Sentiment Analysis Complete:")
    state['messages'].append(f"  Overall Sentiment: {state['sentiment_score']*100:.0f}% positive")
    state['messages'].append(f"  Recent Headlines: {len(state['recent_news'])}")
    
    state['data_sources'].append('News APIs')
    return state

def leadership_culture_analyst(state: CompanyResearchState) -> CompanyResearchState:
    """Analyzes leadership team and company culture"""
    print("👥 Leadership Analyst: Evaluating management and culture...")
    
    # Generate leadership metrics
    state['leadership_info'] = {
        'ceo_tenure': random.randint(2, 15),
        'management_stability': random.choice(['high', 'medium', 'low']),
        'board_independence': round(random.uniform(0.6, 0.9), 2),
        'insider_ownership': round(random.uniform(0.05, 0.25), 2)
    }
    
    # Company culture based on company type
    culture_profiles = {
        "Apple Inc.": "Innovation-focused with emphasis on design excellence and user experience",
        "Tesla": "Mission-driven culture focused on sustainable energy and rapid innovation",
        "Amazon": "Customer-obsessed with high performance standards and data-driven decisions"
    }
    
    state['company_culture'] = culture_profiles.get(
        state['company_name'],
        "Performance-oriented with focus on growth and innovation"
    )
    
    # Employee sentiment
    state['employee_sentiment'] = round(random.uniform(0.65, 0.90), 2)
    
    state['messages'].append(f"✓ Leadership Analysis Complete:")
    state['messages'].append(f"  CEO Tenure: {state['leadership_info']['ceo_tenure']} years")
    state['messages'].append(f"  Employee Satisfaction: {state['employee_sentiment']*100:.0f}%")
    
    state['data_sources'].append('Professional Networks')
    return state

def technology_innovation_analyst(state: CompanyResearchState) -> CompanyResearchState:
    """Analyzes technology stack and innovation capacity"""
    print("🔬 Tech Analyst: Assessing technology and innovation...")
    
    # Tech stacks by company type
    tech_profiles = {
        "Apple Inc.": ["Swift/Objective-C", "Machine Learning", "Custom Silicon", "AR/VR"],
        "Tesla": ["AI/Autopilot", "Battery Technology", "Manufacturing Automation", "OTA Updates"],
        "Amazon": ["AWS Infrastructure", "Machine Learning", "Robotics", "Voice AI"]
    }
    
    state['tech_stack'] = tech_profiles.get(
        state['company_name'],
        ["Cloud Computing", "Data Analytics", "Mobile Apps", "AI/ML"]
    )
    
    # Generate patents
    state['patents'] = [
        f"Advanced {tech} System" 
        for tech in state['tech_stack'][:2]
    ]
    
    # R&D investment as percentage of revenue
    state['rd_investments'] = round(random.uniform(0.08, 0.20), 2)
    
    state['messages'].append(f"✓ Technology Analysis Complete:")
    state['messages'].append(f"  Core Technologies: {', '.join(state['tech_stack'][:2])}")
    state['messages'].append(f"  R&D Investment: {state['rd_investments']*100:.0f}% of revenue")
    
    state['data_sources'].append('Patent Databases')
    return state

def esg_risk_analyst(state: CompanyResearchState) -> CompanyResearchState:
    """Analyzes ESG factors and risk profile"""
    print("🌍 ESG Analyst: Evaluating sustainability and risks...")
    
    # Generate ESG scores
    state['esg_score'] = {
        'environmental': round(random.uniform(0.60, 0.90), 2),
        'social': round(random.uniform(0.65, 0.90), 2),
        'governance': round(random.uniform(0.70, 0.95), 2)
    }
    
    # Risk factors by industry
    risk_profiles = {
        "Technology": [
            "Data privacy regulations",
            "Cybersecurity threats",
            "Supply chain dependencies"
        ],
        "Automotive/Energy": [
            "Environmental regulations",
            "Raw material availability",
            "Technology disruption"
        ],
        "E-commerce/Cloud": [
            "Antitrust regulations",
            "Data center energy usage",
            "Labor relations"
        ]
    }
    
    company_info = COMPANY_DATA.get(state['company_name'], {})
    industry = company_info.get('industry', 'Technology')
    
    state['risk_factors'] = risk_profiles.get(
        industry.split('/')[0],
        ["Market competition", "Regulatory changes", "Economic downturn"]
    )
    
    state['regulatory_issues'] = [
        risk for risk in state['risk_factors'] 
        if 'regulation' in risk.lower()
    ]
    
    avg_esg = sum(state['esg_score'].values()) / 3
    state['messages'].append(f"✓ ESG Analysis Complete:")
    state['messages'].append(f"  Overall ESG Score: {avg_esg*100:.0f}/100")
    state['messages'].append(f"  Key Risks: {len(state['risk_factors'])}")
    
    state['data_sources'].append('ESG Databases')
    return state

def report_synthesizer(state: CompanyResearchState) -> CompanyResearchState:
    """Synthesizes all research into comprehensive report"""
    print("📝 Report Synthesizer: Creating comprehensive analysis...")
    
    # Calculate confidence score
    data_completeness = [
        bool(state.get('financial_metrics')),
        bool(state.get('competitors')),
        bool(state.get('recent_news')),
        bool(state.get('leadership_info')),
        bool(state.get('esg_score')),
        bool(state.get('tech_stack'))
    ]
    state['confidence_score'] = sum(data_completeness) / len(data_completeness)
    
    # Calculate overall score for recommendation
    score_components = {
        'financial': state.get('financial_metrics', {}).get('revenue_growth', 0.1) * 2,
        'market': state.get('market_share', 0.1) * 2,
        'sentiment': state.get('sentiment_score', 0.5),
        'esg': sum(state.get('esg_score', {}).values()) / 3 if state.get('esg_score') else 0.5,
        'innovation': state.get('rd_investments', 0.1) * 3
    }
    
    overall_score = sum(score_components.values()) / len(score_components)
    
    # Generate recommendation
    if overall_score > 0.75:
        state['investment_recommendation'] = "STRONG BUY"
        rec_text = "Exceptional growth potential with strong fundamentals"
    elif overall_score > 0.60:
        state['investment_recommendation'] = "BUY"
        rec_text = "Solid investment opportunity with good upside"
    elif overall_score > 0.45:
        state['investment_recommendation'] = "HOLD"
        rec_text = "Stable investment with moderate growth prospects"
    else:
        state['investment_recommendation'] = "UNDERWEIGHT"
        rec_text = "Consider reducing exposure due to concerns"
    
    # Generate executive summary
    state['executive_summary'] = f"""
📊 EXECUTIVE SUMMARY - {state['company_name']} ({state.get('ticker', 'N/A')})
{'='*60}

📈 FINANCIAL PERFORMANCE
• Revenue: ${state.get('financial_metrics', {}).get('revenue', 0)/1e9:.1f}B
• Growth Rate: {state.get('financial_metrics', {}).get('revenue_growth', 0)*100:.0f}%
• Profit Margin: {state.get('financial_metrics', {}).get('profit_margin', 0)*100:.0f}%
• P/E Ratio: {state.get('financial_metrics', {}).get('pe_ratio', 'N/A')}

🏆 MARKET POSITION
• Market Share: {state.get('market_share', 0)*100:.0f}%
• Key Competitors: {', '.join(state.get('competitors', [])[:3])}

💡 COMPETITIVE ADVANTAGES
{chr(10).join(f'• {adv}' for adv in state.get('competitive_advantages', [])[:3])}

📰 MARKET SENTIMENT
• Sentiment Score: {state.get('sentiment_score', 0)*100:.0f}% positive
• Recent Developments: {len(state.get('key_events', []))} positive events

🌍 ESG RATING
• Environmental: {state.get('esg_score', {}).get('environmental', 0)*100:.0f}/100
• Social: {state.get('esg_score', {}).get('social', 0)*100:.0f}/100
• Governance: {state.get('esg_score', {}).get('governance', 0)*100:.0f}/100

⚠️ KEY RISKS
{chr(10).join(f'• {risk}' for risk in state.get('risk_factors', [])[:3])}

💼 INVESTMENT RECOMMENDATION: {state['investment_recommendation']}
{rec_text}

📊 Research Confidence: {state['confidence_score']*100:.0f}%
📚 Data Sources: {len(set(state['data_sources']))} verified sources
"""
    
    state['messages'].append(f"✓ Report Synthesis Complete")
    state['messages'].append(f"  Recommendation: {state['investment_recommendation']}")
    state['messages'].append(f"  Confidence Score: {state['confidence_score']*100:.0f}%")
    
    return state

def quality_validator(state: CompanyResearchState) -> CompanyResearchState:
    """Validates research quality and completeness"""
    print("✅ Quality Validator: Checking research completeness...")
    
    # Check critical data points
    validations = {
        'Financial Data': bool(state.get('financial_metrics')),
        'Market Analysis': bool(state.get('competitors')),
        'News Sentiment': bool(state.get('recent_news')),
        'Risk Assessment': bool(state.get('risk_factors')),
        'ESG Analysis': bool(state.get('esg_score'))
    }
    
    missing = [check for check, valid in validations.items() if not valid]
    
    if missing:
        state['errors'].extend([f"Missing: {item}" for item in missing])
        state['messages'].append(f"⚠️ Quality Check: {len(missing)} data points missing")
    else:
        state['messages'].append("✅ Quality Check: All critical data points collected")
    
    # Add final validation message
    state['messages'].append(f"✓ Research validation complete")
    
    return state

# Routing functions
def should_enhance_research(state: CompanyResearchState) -> Literal["enhance", "complete"]:
    """Determines if additional research is needed"""
    if state['confidence_score'] < 0.7 and len(state.get('errors', [])) == 0:
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
    
    # Sequential flow to avoid parallel writes
    builder.add_edge("company_identifier", "financial_analyst")
    builder.add_edge("financial_analyst", "market_analyst")
    builder.add_edge("market_analyst", "news_sentiment_analyst")
    
    # Continue with specialized analysis
    builder.add_edge("news_sentiment_analyst", "leadership_culture_analyst")
    builder.add_edge("leadership_culture_analyst", "technology_innovation_analyst")
    builder.add_edge("technology_innovation_analyst", "esg_risk_analyst")
    
    # Convergence at synthesis
    builder.add_edge("esg_risk_analyst", "report_synthesizer")
    
    # Quality validation
    builder.add_edge("report_synthesizer", "quality_validator")
    
    # Conditional completion
    builder.add_conditional_edges(
        "quality_validator",
        should_enhance_research,
        {
            "enhance": "market_analyst",
            "complete": END
        }
    )
    
    return builder.compile()

# Demo execution
if __name__ == "__main__":
    # Create the research graph
    graph = create_company_research_graph()
    
    # Save visualization
    try:
        img = Image(graph.get_graph().draw_mermaid_png())
        with open("company_research_graph.png", "wb") as f:
            f.write(img.data)
        print("📊 Graph visualization saved!")
    except Exception as e:
        print(f"Visualization error: {e}")
    
    # Print Mermaid diagram
    print("\n🎨 Mermaid Diagram:")
    print(graph.get_graph().draw_mermaid())
    
    # Run research on companies
    print("\n" + "="*70)
    print("🔍 LANGGRAPH COMPANY RESEARCH SYSTEM")
    print("="*70)
    
    test_companies = ["Apple Inc.", "Tesla", "Amazon"]
    
    for company_name in test_companies:
        print(f"\n{'='*70}")
        print(f"🏢 RESEARCHING: {company_name}")
        print(f"{'='*70}")
        
        initial_state = {
            "company_name": company_name,
            "ticker": "",
            "research_objective": "Investment analysis",
            "research_depth": "standard",
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
        
        # Run the research workflow
        result = graph.invoke(initial_state)
        
        # Display executive summary
        print(result['executive_summary'])
        
        # Show workflow steps
        print("\n🔄 RESEARCH WORKFLOW STEPS:")
        for msg in result['messages']:
            print(f"  {msg}")
        
        print(f"\n{'='*70}")