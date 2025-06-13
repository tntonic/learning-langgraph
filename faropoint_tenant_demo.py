"""
Faropoint Tenant Research System - Demo Version (No API Required)
Simulates tenant research workflow for commercial real estate
"""

from typing import TypedDict, Literal, List, Dict, Any, Annotated, Optional
from langgraph.graph import StateGraph, START, END
from datetime import datetime
import json
import operator
import random
import re

# Define the state for tenant research
class TenantResearchState(TypedDict):
    # Company Information
    company_name: str
    location: str
    industry: str
    
    # Online Presence
    website_url: Optional[str]
    social_media_profiles: Dict[str, str]
    online_reviews: List[Dict]
    review_sentiment: float
    
    # Business Verification
    business_registration: Dict[str, Any]
    years_in_business: Optional[int]
    business_type: str
    is_verified: bool
    
    # Financial Indicators
    estimated_revenue: Optional[str]
    employee_count: Optional[str]
    growth_indicators: List[str]
    
    # Real Estate Relevant
    current_locations: List[str]
    space_requirements: Optional[str]
    lease_history: List[Dict]
    
    # Risk Assessment
    litigation_history: List[str]
    bankruptcy_flags: bool
    negative_news: List[str]
    risk_score: float
    
    # Tenant Quality Score
    creditworthiness_indicators: List[str]
    stability_score: float
    growth_potential: float
    overall_tenant_score: float
    
    # Final Outputs
    recommendation: Literal["Highly Recommended", "Recommended", "Proceed with Caution", "Not Recommended"]
    executive_summary: str
    key_concerns: List[str]
    positive_factors: List[str]
    
    # Workflow Management
    messages: Annotated[List[str], operator.add]
    data_sources: List[str]
    confidence_level: float

# Simulated data for demo
DEMO_COMPANY_DATA = {
    "Blue Bottle Coffee": {
        "industry": "Food & Beverage",
        "website": "https://bluebottlecoffee.com",
        "founded": 2002,
        "employees": "500-1000",
        "revenue": "$100M+",
        "locations": ["Ferry Building, San Francisco", "Oakland Headquarters"],
        "social_media": {"instagram": "@bluebottle", "linkedin": "blue-bottle-coffee"},
        "review_score": 4.5,
        "risk_factors": []
    },
    "TechVenture Labs": {
        "industry": "Technology",
        "website": "https://techventurelabs.io",
        "founded": 2019,
        "employees": "10-50",
        "revenue": "$5-10M",
        "locations": ["WeWork Palo Alto"],
        "social_media": {"linkedin": "techventure-labs"},
        "review_score": 3.8,
        "risk_factors": ["New business", "Limited financial history"]
    },
    "GreenSpace Wellness": {
        "industry": "Health & Wellness",
        "website": None,
        "founded": 2021,
        "employees": "5-10",
        "revenue": "Under $1M",
        "locations": [],
        "social_media": {"instagram": "@greenspacewellness"},
        "review_score": 4.2,
        "risk_factors": ["Very new business", "No verified location", "Limited online presence"]
    }
}

def company_identifier_agent(state: TenantResearchState) -> TenantResearchState:
    """Simulates company identification"""
    print(f"🔍 Identifying company: {state['company_name']}...")
    
    # Simulate finding company data
    company_data = DEMO_COMPANY_DATA.get(state['company_name'], {})
    
    if company_data:
        state['industry'] = company_data.get('industry', 'Unknown')
        state['website_url'] = company_data.get('website')
        state['messages'].append(f"✓ Found company profile for {state['company_name']}")
        if state['website_url']:
            state['messages'].append(f"✓ Website: {state['website_url']}")
    else:
        # Simulate unknown company
        state['industry'] = "Unknown"
        state['messages'].append(f"⚠️ Limited information available for {state['company_name']}")
    
    state['data_sources'].append("Business Database Search")
    return state

def online_presence_analyzer(state: TenantResearchState) -> TenantResearchState:
    """Simulates online presence analysis"""
    print("🌐 Analyzing online presence...")
    
    company_data = DEMO_COMPANY_DATA.get(state['company_name'], {})
    
    # Social media profiles
    state['social_media_profiles'] = company_data.get('social_media', {})
    if state['social_media_profiles']:
        state['messages'].append(f"✓ Found {len(state['social_media_profiles'])} social media profiles")
    
    # Review sentiment
    review_score = company_data.get('review_score', random.uniform(3.0, 4.5))
    state['review_sentiment'] = review_score / 5.0  # Normalize to 0-1
    
    # Simulate reviews
    state['online_reviews'] = [
        {
            "source": "Google",
            "rating": review_score,
            "count": random.randint(10, 200),
            "summary": "Generally positive" if review_score > 4 else "Mixed reviews"
        }
    ]
    
    state['messages'].append(f"✓ Review sentiment: {state['review_sentiment']:.2f} ({review_score:.1f}/5.0)")
    state['data_sources'].append("Online Review Platforms")
    
    return state

def business_verification_agent(state: TenantResearchState) -> TenantResearchState:
    """Simulates business verification"""
    print("📋 Verifying business registration...")
    
    company_data = DEMO_COMPANY_DATA.get(state['company_name'], {})
    
    # Determine business type
    if "LLC" in state['company_name']:
        state['business_type'] = "LLC"
    elif "Inc" in state['company_name'] or "Corp" in state['company_name']:
        state['business_type'] = "Corporation"
    else:
        state['business_type'] = "LLC"  # Default assumption
    
    # Years in business
    if 'founded' in company_data:
        state['years_in_business'] = datetime.now().year - company_data['founded']
        state['is_verified'] = True
        state['messages'].append(f"✓ Verified: {state['years_in_business']} years in business")
    else:
        state['years_in_business'] = random.randint(1, 5)
        state['is_verified'] = random.choice([True, False])
        if state['is_verified']:
            state['messages'].append("✓ Business registration verified")
        else:
            state['messages'].append("⚠️ Could not verify business registration")
    
    state['data_sources'].append("State Business Registry")
    return state

def financial_indicators_agent(state: TenantResearchState) -> TenantResearchState:
    """Simulates financial analysis"""
    print("💰 Analyzing financial indicators...")
    
    company_data = DEMO_COMPANY_DATA.get(state['company_name'], {})
    
    # Revenue and employees
    state['estimated_revenue'] = company_data.get('revenue', "Not disclosed")
    state['employee_count'] = company_data.get('employees', "Unknown")
    
    # Growth indicators
    if state['years_in_business'] and state['years_in_business'] < 5:
        state['growth_indicators'] = ["Young growing company", "Expanding team"]
    elif state['estimated_revenue'] and "100M" in state['estimated_revenue']:
        state['growth_indicators'] = ["Strong revenue", "Market leader", "Stable growth"]
    else:
        state['growth_indicators'] = ["Steady operations"]
    
    state['messages'].append(f"✓ Revenue estimate: {state['estimated_revenue']}")
    state['messages'].append(f"✓ Employee count: {state['employee_count']}")
    state['data_sources'].append("Financial Indicators Analysis")
    
    return state

def real_estate_history_agent(state: TenantResearchState) -> TenantResearchState:
    """Simulates real estate history research"""
    print("🏢 Researching real estate history...")
    
    company_data = DEMO_COMPANY_DATA.get(state['company_name'], {})
    
    # Current locations
    state['current_locations'] = company_data.get('locations', [])
    if state['current_locations']:
        state['messages'].append(f"✓ Found {len(state['current_locations'])} current location(s)")
    else:
        state['messages'].append("⚠️ No verified locations found")
    
    # Space requirements (simulate based on employee count)
    if state['employee_count'] and state['employee_count'] != "Unknown":
        if "500" in state['employee_count']:
            state['space_requirements'] = "20,000-50,000 sq ft"
        elif "50" in state['employee_count']:
            state['space_requirements'] = "5,000-10,000 sq ft"
        else:
            state['space_requirements'] = "1,000-5,000 sq ft"
        state['messages'].append(f"✓ Estimated space needs: {state['space_requirements']}")
    
    # Lease history
    if state['current_locations']:
        state['lease_history'] = [{"type": "Current lease", "status": "Active"}]
    
    state['data_sources'].append("Commercial Real Estate Records")
    return state

def risk_assessment_agent(state: TenantResearchState) -> TenantResearchState:
    """Simulates risk assessment"""
    print("⚠️ Performing risk assessment...")
    
    company_data = DEMO_COMPANY_DATA.get(state['company_name'], {})
    risk_factors = company_data.get('risk_factors', [])
    
    # Litigation (simulate)
    state['litigation_history'] = []
    state['bankruptcy_flags'] = False
    
    # Negative news
    state['negative_news'] = risk_factors
    
    # Calculate risk score
    risk_points = 0
    
    if state['years_in_business'] and state['years_in_business'] < 2:
        risk_points += 3
        state['negative_news'].append("Very new business")
    
    if not state['is_verified']:
        risk_points += 2
        
    if not state['website_url']:
        risk_points += 1
        
    if len(state['current_locations']) == 0:
        risk_points += 2
        
    risk_points += len(risk_factors) * 0.5
    
    state['risk_score'] = min(risk_points / 10, 1.0)
    state['messages'].append(f"✓ Risk assessment complete: {state['risk_score']:.2f}")
    
    if state['negative_news']:
        state['messages'].append(f"⚠️ Risk factors: {', '.join(state['negative_news'][:2])}")
    
    state['data_sources'].append("Risk Assessment Database")
    return state

def tenant_scoring_agent(state: TenantResearchState) -> TenantResearchState:
    """Calculates tenant scores"""
    print("📊 Calculating tenant scores...")
    
    # Creditworthiness indicators
    state['creditworthiness_indicators'] = []
    
    if state['estimated_revenue'] != "Not disclosed":
        state['creditworthiness_indicators'].append("Revenue verified")
    if state['years_in_business'] and state['years_in_business'] > 3:
        state['creditworthiness_indicators'].append(f"Established ({state['years_in_business']} years)")
    if state['is_verified']:
        state['creditworthiness_indicators'].append("Verified entity")
    if state['review_sentiment'] > 0.7:
        state['creditworthiness_indicators'].append("Strong reputation")
    if state['current_locations']:
        state['creditworthiness_indicators'].append("Existing tenant")
    
    # Stability score
    stability_components = {
        'years': min((state['years_in_business'] or 0) / 10, 1.0) * 0.3,
        'verified': 0.2 if state['is_verified'] else 0,
        'locations': 0.2 if state['current_locations'] else 0,
        'online': len(state['social_media_profiles']) / 5 * 0.3
    }
    state['stability_score'] = sum(stability_components.values())
    
    # Growth potential
    growth_components = {
        'indicators': len(state['growth_indicators']) / 5 * 0.4,
        'reviews': max(0, (state['review_sentiment'] - 0.5) * 2) * 0.3,
        'size': 0.3 if state['employee_count'] != "Unknown" else 0
    }
    state['growth_potential'] = sum(growth_components.values())
    
    # Overall score
    score_components = {
        'stability': state['stability_score'] * 30,
        'growth': state['growth_potential'] * 20,
        'reputation': state['review_sentiment'] * 25,
        'risk': (1 - state['risk_score']) * 25
    }
    state['overall_tenant_score'] = sum(score_components.values())
    
    # Recommendation
    if state['overall_tenant_score'] >= 75:
        state['recommendation'] = "Highly Recommended"
    elif state['overall_tenant_score'] >= 60:
        state['recommendation'] = "Recommended"
    elif state['overall_tenant_score'] >= 40:
        state['recommendation'] = "Proceed with Caution"
    else:
        state['recommendation'] = "Not Recommended"
    
    # Key factors
    state['key_concerns'] = []
    state['positive_factors'] = []
    
    if state['risk_score'] > 0.5:
        state['key_concerns'].append("Elevated risk profile")
    if state['years_in_business'] and state['years_in_business'] < 2:
        state['key_concerns'].append("Very new business")
    if not state['current_locations']:
        state['key_concerns'].append("No verified locations")
    
    if state['stability_score'] > 0.7:
        state['positive_factors'].append("High stability")
    if state['review_sentiment'] > 0.8:
        state['positive_factors'].append("Excellent reputation")
    if state['growth_indicators']:
        state['positive_factors'].append("Growth potential")
    
    state['messages'].append(f"✓ Tenant score: {state['overall_tenant_score']:.1f}/100")
    state['messages'].append(f"✓ Recommendation: {state['recommendation']}")
    
    return state

def report_generator_agent(state: TenantResearchState) -> TenantResearchState:
    """Generates final report"""
    print("📝 Generating report...")
    
    # Confidence level
    data_completeness = [
        state['website_url'] is not None,
        bool(state['social_media_profiles']),
        state['years_in_business'] is not None,
        state['estimated_revenue'] != "Not disclosed",
        bool(state['current_locations']),
        state['is_verified']
    ]
    state['confidence_level'] = sum(data_completeness) / len(data_completeness)
    
    # Executive summary
    state['executive_summary'] = f"""
🏢 TENANT EVALUATION: {state['company_name']}
{'='*60}
Location: {state['location']} | Industry: {state['industry']}

⭐ RECOMMENDATION: {state['recommendation']}
📊 Tenant Score: {state['overall_tenant_score']:.1f}/100

KEY METRICS:
• Years in Business: {state['years_in_business'] or 'Unknown'}
• Business Type: {state['business_type']}
• Verification: {'✓ Verified' if state['is_verified'] else '⚠️ Unverified'}
• Revenue: {state['estimated_revenue']}
• Employees: {state['employee_count']}
• Current Locations: {len(state['current_locations'])}

SCORES:
• Stability: {state['stability_score']:.2f}/1.0
• Growth Potential: {state['growth_potential']:.2f}/1.0
• Risk Level: {state['risk_score']:.2f}/1.0 (lower is better)
• Online Reputation: {state['review_sentiment']:.2f}/1.0

{'🟢 STRENGTHS:' if state['positive_factors'] else ''}
{chr(10).join(f'  • {f}' for f in state['positive_factors'])}

{'🔴 CONCERNS:' if state['key_concerns'] else ''}
{chr(10).join(f'  • {c}' for c in state['key_concerns'])}

📈 Confidence Level: {state['confidence_level']*100:.0f}%
📚 Data Sources: {len(set(state['data_sources']))}
"""
    
    state['messages'].append("✓ Report complete")
    return state

# Build the workflow
def create_tenant_research_graph():
    builder = StateGraph(TenantResearchState)
    
    # Add nodes
    builder.add_node("identify", company_identifier_agent)
    builder.add_node("online", online_presence_analyzer)
    builder.add_node("verify", business_verification_agent)
    builder.add_node("financial", financial_indicators_agent)
    builder.add_node("real_estate", real_estate_history_agent)
    builder.add_node("risk", risk_assessment_agent)
    builder.add_node("score", tenant_scoring_agent)
    builder.add_node("report", report_generator_agent)
    
    # Define flow
    builder.add_edge(START, "identify")
    builder.add_edge("identify", "online")
    builder.add_edge("online", "verify")
    builder.add_edge("verify", "financial")
    builder.add_edge("financial", "real_estate")
    builder.add_edge("real_estate", "risk")
    builder.add_edge("risk", "score")
    builder.add_edge("score", "report")
    builder.add_edge("report", END)
    
    return builder.compile()

# Main execution
if __name__ == "__main__":
    from IPython.display import Image, display
    
    # Create graph
    graph = create_tenant_research_graph()
    
    # Save visualization
    try:
        img = Image(graph.get_graph().draw_mermaid_png())
        with open("faropoint_workflow.png", "wb") as f:
            f.write(img.data)
        print("📊 Workflow diagram saved!")
    except:
        pass
    
    print("\n🎨 Tenant Research Workflow:")
    print(graph.get_graph().draw_mermaid())
    
    # Demo companies
    print("\n" + "="*70)
    print("🏢 FAROPOINT TENANT RESEARCH SYSTEM - DEMO")
    print("="*70)
    
    test_companies = [
        {"name": "Blue Bottle Coffee", "location": "Oakland, CA"},
        {"name": "TechVenture Labs", "location": "Palo Alto, CA"},
        {"name": "GreenSpace Wellness", "location": "San Francisco, CA"},
    ]
    
    for company in test_companies:
        print(f"\n{'='*70}")
        print(f"Researching: {company['name']}")
        print(f"{'='*70}")
        
        initial_state = {
            "company_name": company['name'],
            "location": company['location'],
            "industry": "",
            "website_url": None,
            "social_media_profiles": {},
            "online_reviews": [],
            "review_sentiment": 0.5,
            "business_registration": {},
            "years_in_business": None,
            "business_type": "",
            "is_verified": False,
            "estimated_revenue": None,
            "employee_count": None,
            "growth_indicators": [],
            "current_locations": [],
            "space_requirements": None,
            "lease_history": [],
            "litigation_history": [],
            "bankruptcy_flags": False,
            "negative_news": [],
            "risk_score": 0.5,
            "creditworthiness_indicators": [],
            "stability_score": 0.0,
            "growth_potential": 0.0,
            "overall_tenant_score": 0.0,
            "recommendation": "Not Recommended",
            "executive_summary": "",
            "key_concerns": [],
            "positive_factors": [],
            "messages": [],
            "data_sources": [],
            "confidence_level": 0.0
        }
        
        # Run research
        result = graph.invoke(initial_state)
        
        # Display report
        print(result['executive_summary'])
        
        # Show process
        print("\n📋 Research Process:")
        for msg in result['messages']:
            print(f"  {msg}")