"""
Faropoint Tenant Research System - LangGraph Implementation
Analyzes small private companies as potential tenants for commercial real estate
Uses web search and analysis to gather intelligence on businesses
"""

import os
from typing import TypedDict, Literal, List, Dict, Any, Annotated, Optional
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.document_loaders import WebBaseLoader
from datetime import datetime
import json
import operator
import re
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup

# Initialize tools
search_tool = DuckDuckGoSearchRun()
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

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
    business_type: str  # LLC, Corp, etc.
    is_verified: bool
    
    # Financial Indicators (from public data)
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
    risk_score: float  # 0-1, lower is better
    
    # Tenant Quality Score
    creditworthiness_indicators: List[str]
    stability_score: float  # 0-1, higher is better
    growth_potential: float  # 0-1
    overall_tenant_score: float  # 0-100
    
    # Final Outputs
    recommendation: Literal["Highly Recommended", "Recommended", "Proceed with Caution", "Not Recommended"]
    executive_summary: str
    detailed_report: str
    key_concerns: List[str]
    positive_factors: List[str]
    
    # Workflow Management
    messages: Annotated[List[str], operator.add]
    data_sources: List[str]
    search_queries_used: List[str]
    confidence_level: float

# Agent functions

def company_identifier_agent(state: TenantResearchState) -> TenantResearchState:
    """Identifies the company and gathers basic information"""
    print(f"🔍 Identifying company: {state['company_name']} in {state['location']}...")
    
    # Search for company information
    search_query = f"{state['company_name']} {state['location']} company business"
    state['search_queries_used'].append(search_query)
    
    try:
        search_results = search_tool.run(search_query)
        state['data_sources'].append("DuckDuckGo Search")
        
        # Use LLM to extract company info
        prompt = f"""
        Extract company information from these search results:
        {search_results[:1000]}
        
        For company: {state['company_name']}
        Location: {state['location']}
        
        Extract:
        1. Industry/Business Type
        2. Any website URL mentioned
        3. Years in business or founding date
        4. Business type (LLC, Corp, etc)
        
        Format as JSON.
        """
        
        response = llm.invoke([SystemMessage(content=prompt)])
        
        # Update state with findings
        state['messages'].append(f"✓ Initial search completed for {state['company_name']}")
        
        # Try to extract website
        url_pattern = r'https?://(?:www\.)?[\w\-\.]+\.(?:com|net|org|biz|info|co)'
        urls = re.findall(url_pattern, search_results)
        if urls:
            state['website_url'] = urls[0]
            state['messages'].append(f"✓ Found website: {urls[0]}")
            
    except Exception as e:
        state['messages'].append(f"⚠️ Error in initial search: {str(e)}")
    
    return state

def online_presence_analyzer(state: TenantResearchState) -> TenantResearchState:
    """Analyzes the company's online presence and reputation"""
    print("🌐 Analyzing online presence...")
    
    # Search for social media profiles
    social_search = f"{state['company_name']} {state['location']} LinkedIn Facebook Instagram"
    state['search_queries_used'].append(social_search)
    
    try:
        social_results = search_tool.run(social_search)
        
        # Extract social media URLs
        social_patterns = {
            'linkedin': r'linkedin\.com/company/[\w\-]+',
            'facebook': r'facebook\.com/[\w\-\.]+',
            'instagram': r'instagram\.com/[\w\-\.]+',
            'twitter': r'twitter\.com/[\w\-]+'
        }
        
        state['social_media_profiles'] = {}
        for platform, pattern in social_patterns.items():
            matches = re.findall(pattern, social_results)
            if matches:
                state['social_media_profiles'][platform] = f"https://{matches[0]}"
        
        if state['social_media_profiles']:
            state['messages'].append(f"✓ Found {len(state['social_media_profiles'])} social media profiles")
        
        # Search for reviews
        review_search = f"{state['company_name']} {state['location']} reviews Google Yelp"
        state['search_queries_used'].append(review_search)
        review_results = search_tool.run(review_search)
        
        # Extract review information
        prompt = f"""
        Extract review information from these search results:
        {review_results[:1000]}
        
        Look for:
        1. Average rating (out of 5)
        2. Number of reviews
        3. Common positive themes
        4. Common complaints
        5. Overall sentiment (positive/neutral/negative)
        
        Format as JSON with 'rating', 'review_count', 'positive_themes', 'negative_themes', 'sentiment'
        """
        
        review_response = llm.invoke([SystemMessage(content=prompt)])
        
        # Simple sentiment scoring
        if "positive" in review_results.lower():
            state['review_sentiment'] = 0.7
        elif "negative" in review_results.lower():
            state['review_sentiment'] = 0.3
        else:
            state['review_sentiment'] = 0.5
            
        state['messages'].append(f"✓ Review sentiment score: {state['review_sentiment']:.2f}")
        state['data_sources'].append("Online Reviews")
        
    except Exception as e:
        state['messages'].append(f"⚠️ Error analyzing online presence: {str(e)}")
        state['review_sentiment'] = 0.5  # neutral default
    
    return state

def business_verification_agent(state: TenantResearchState) -> TenantResearchState:
    """Verifies business registration and legitimacy"""
    print("📋 Verifying business registration...")
    
    # Search for business registration
    registration_search = f"{state['company_name']} {state['location']} Secretary of State business registration LLC corporation"
    state['search_queries_used'].append(registration_search)
    
    try:
        registration_results = search_tool.run(registration_search)
        
        # Check for business entity indicators
        entity_types = ['LLC', 'Corporation', 'Corp', 'Inc', 'Limited', 'Partnership', 'LLP']
        for entity in entity_types:
            if entity.lower() in registration_results.lower():
                state['business_type'] = entity
                break
        
        # Look for registration indicators
        if any(term in registration_results.lower() for term in ['registered', 'incorporated', 'established']):
            state['is_verified'] = True
            state['messages'].append("✓ Business registration verified")
        else:
            state['is_verified'] = False
            state['messages'].append("⚠️ Could not verify business registration")
        
        # Extract years in business
        year_patterns = [
            r'established (\d{4})',
            r'founded (\d{4})',
            r'since (\d{4})',
            r'incorporated (\d{4})'
        ]
        
        for pattern in year_patterns:
            matches = re.findall(pattern, registration_results.lower())
            if matches:
                founding_year = int(matches[0])
                state['years_in_business'] = datetime.now().year - founding_year
                state['messages'].append(f"✓ Years in business: {state['years_in_business']}")
                break
        
        state['data_sources'].append("Business Registration Search")
        
    except Exception as e:
        state['messages'].append(f"⚠️ Error in business verification: {str(e)}")
        state['is_verified'] = False
    
    return state

def financial_indicators_agent(state: TenantResearchState) -> TenantResearchState:
    """Gathers financial indicators from public sources"""
    print("💰 Analyzing financial indicators...")
    
    # Search for revenue and employee information
    financial_search = f"{state['company_name']} {state['location']} revenue employees annual sales"
    state['search_queries_used'].append(financial_search)
    
    try:
        financial_results = search_tool.run(financial_search)
        
        # Extract revenue indicators
        revenue_patterns = [
            r'\$(\d+(?:\.\d+)?)\s*(?:million|M)',
            r'\$(\d+(?:\.\d+)?)\s*(?:billion|B)',
            r'\$(\d+(?:,\d+)*)\s*(?:in revenue|annual revenue|sales)',
            r'revenue of \$(\d+(?:,\d+)*)'
        ]
        
        for pattern in revenue_patterns:
            matches = re.findall(pattern, financial_results)
            if matches:
                state['estimated_revenue'] = matches[0]
                state['messages'].append(f"✓ Estimated revenue found: ${matches[0]}")
                break
        
        # Extract employee count
        employee_patterns = [
            r'(\d+)\s*employees',
            r'(\d+)\s*staff',
            r'team of (\d+)',
            r'(\d+)-(\d+)\s*employees'
        ]
        
        for pattern in employee_patterns:
            matches = re.findall(pattern, financial_results)
            if matches:
                if isinstance(matches[0], tuple):
                    state['employee_count'] = f"{matches[0][0]}-{matches[0][1]}"
                else:
                    state['employee_count'] = matches[0]
                state['messages'].append(f"✓ Employee count: {state['employee_count']}")
                break
        
        # Look for growth indicators
        growth_keywords = ['expanding', 'growth', 'hiring', 'new location', 'increased revenue', 'record sales']
        state['growth_indicators'] = [kw for kw in growth_keywords if kw in financial_results.lower()]
        
        if state['growth_indicators']:
            state['messages'].append(f"✓ Growth indicators: {', '.join(state['growth_indicators'])}")
        
        state['data_sources'].append("Financial Indicators Search")
        
    except Exception as e:
        state['messages'].append(f"⚠️ Error gathering financial indicators: {str(e)}")
    
    return state

def real_estate_history_agent(state: TenantResearchState) -> TenantResearchState:
    """Researches real estate and lease history"""
    print("🏢 Researching real estate history...")
    
    # Search for current locations and lease history
    location_search = f"{state['company_name']} {state['location']} office location address lease space"
    state['search_queries_used'].append(location_search)
    
    try:
        location_results = search_tool.run(location_search)
        
        # Extract addresses
        address_pattern = r'\d+\s+[\w\s]+(?:Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd|Drive|Dr|Lane|Ln|Way|Parkway|Pkwy)'
        addresses = re.findall(address_pattern, location_results)
        
        if addresses:
            state['current_locations'] = list(set(addresses[:3]))  # Keep top 3 unique
            state['messages'].append(f"✓ Found {len(state['current_locations'])} location(s)")
        
        # Look for space requirements indicators
        space_patterns = [
            r'(\d+(?:,\d+)?)\s*(?:square feet|sq ft|sf)',
            r'(\d+(?:,\d+)?)\s*(?:square meters|sq m)',
        ]
        
        for pattern in space_patterns:
            matches = re.findall(pattern, location_results)
            if matches:
                state['space_requirements'] = f"{matches[0]} sq ft"
                state['messages'].append(f"✓ Space requirement indicator: {state['space_requirements']}")
                break
        
        # Search for lease or relocation history
        lease_search = f"{state['company_name']} moved relocated new office expansion"
        state['search_queries_used'].append(lease_search)
        lease_results = search_tool.run(lease_search)
        
        # Simple lease history based on keywords
        if 'moved' in lease_results.lower() or 'relocated' in lease_results.lower():
            state['lease_history'].append({
                'event': 'Recent relocation detected',
                'details': 'Company has moved offices recently'
            })
        
        state['data_sources'].append("Real Estate History Search")
        
    except Exception as e:
        state['messages'].append(f"⚠️ Error researching real estate history: {str(e)}")
    
    return state

def risk_assessment_agent(state: TenantResearchState) -> TenantResearchState:
    """Performs risk assessment including litigation and bankruptcy checks"""
    print("⚠️ Performing risk assessment...")
    
    # Search for litigation
    litigation_search = f"{state['company_name']} lawsuit litigation sued court case"
    state['search_queries_used'].append(litigation_search)
    
    try:
        litigation_results = search_tool.run(litigation_search)
        
        # Check for litigation keywords
        litigation_keywords = ['lawsuit', 'sued', 'litigation', 'court case', 'legal action', 'defendant']
        found_litigation = [kw for kw in litigation_keywords if kw in litigation_results.lower()]
        
        if found_litigation:
            state['litigation_history'].append(f"Potential litigation found: {', '.join(found_litigation)}")
            state['messages'].append("⚠️ Litigation indicators detected")
        
        # Search for bankruptcy
        bankruptcy_search = f"{state['company_name']} bankruptcy Chapter 7 Chapter 11 financial distress"
        state['search_queries_used'].append(bankruptcy_search)
        bankruptcy_results = search_tool.run(bankruptcy_search)
        
        bankruptcy_keywords = ['bankruptcy', 'chapter 7', 'chapter 11', 'insolvent', 'financial distress']
        if any(kw in bankruptcy_results.lower() for kw in bankruptcy_keywords):
            state['bankruptcy_flags'] = True
            state['messages'].append("🚨 Bankruptcy indicators detected")
        else:
            state['bankruptcy_flags'] = False
        
        # Search for negative news
        negative_search = f"{state['company_name']} scandal problem issue complaint violation"
        state['search_queries_used'].append(negative_search)
        negative_results = search_tool.run(negative_search)
        
        negative_keywords = ['scandal', 'violation', 'fine', 'penalty', 'complaint', 'investigation']
        found_negative = [kw for kw in negative_keywords if kw in negative_results.lower()]
        
        if found_negative:
            state['negative_news'] = found_negative
            state['messages'].append(f"⚠️ Negative news indicators: {', '.join(found_negative)}")
        
        # Calculate risk score
        risk_factors = 0
        if state['litigation_history']:
            risk_factors += 2
        if state['bankruptcy_flags']:
            risk_factors += 3
        if state['negative_news']:
            risk_factors += len(state['negative_news']) * 0.5
        if not state['is_verified']:
            risk_factors += 1
        
        # Normalize to 0-1 scale
        state['risk_score'] = min(risk_factors / 10, 1.0)
        state['messages'].append(f"✓ Risk score calculated: {state['risk_score']:.2f}")
        
        state['data_sources'].append("Risk Assessment Search")
        
    except Exception as e:
        state['messages'].append(f"⚠️ Error in risk assessment: {str(e)}")
        state['risk_score'] = 0.5  # Default medium risk
    
    return state

def tenant_scoring_agent(state: TenantResearchState) -> TenantResearchState:
    """Calculates overall tenant quality scores"""
    print("📊 Calculating tenant scores...")
    
    # Creditworthiness indicators
    state['creditworthiness_indicators'] = []
    
    if state.get('estimated_revenue'):
        state['creditworthiness_indicators'].append("Revenue data available")
    if state.get('years_in_business', 0) > 3:
        state['creditworthiness_indicators'].append(f"Established business ({state['years_in_business']} years)")
    if state['is_verified']:
        state['creditworthiness_indicators'].append("Verified business entity")
    if state['review_sentiment'] > 0.6:
        state['creditworthiness_indicators'].append("Positive online reputation")
    if not state['bankruptcy_flags']:
        state['creditworthiness_indicators'].append("No bankruptcy indicators")
    
    # Calculate stability score
    stability_factors = {
        'years_in_business': min(state.get('years_in_business', 0) / 10, 1.0) * 0.3,
        'verified_business': 0.2 if state['is_verified'] else 0,
        'online_presence': len(state['social_media_profiles']) / 4 * 0.2,
        'no_bankruptcy': 0.3 if not state['bankruptcy_flags'] else 0
    }
    state['stability_score'] = sum(stability_factors.values())
    
    # Calculate growth potential
    growth_factors = {
        'growth_indicators': len(state['growth_indicators']) / 5 * 0.4,
        'positive_reviews': max(0, (state['review_sentiment'] - 0.5) * 2) * 0.3,
        'employee_count': 0.3 if state.get('employee_count') else 0
    }
    state['growth_potential'] = sum(growth_factors.values())
    
    # Calculate overall tenant score (0-100)
    score_components = {
        'stability': state['stability_score'] * 30,
        'growth': state['growth_potential'] * 20,
        'reputation': state['review_sentiment'] * 20,
        'risk': (1 - state['risk_score']) * 30
    }
    
    state['overall_tenant_score'] = sum(score_components.values())
    
    # Determine recommendation
    if state['overall_tenant_score'] >= 75:
        state['recommendation'] = "Highly Recommended"
    elif state['overall_tenant_score'] >= 60:
        state['recommendation'] = "Recommended"
    elif state['overall_tenant_score'] >= 40:
        state['recommendation'] = "Proceed with Caution"
    else:
        state['recommendation'] = "Not Recommended"
    
    # Identify key concerns and positive factors
    state['key_concerns'] = []
    state['positive_factors'] = []
    
    # Concerns
    if state['risk_score'] > 0.5:
        state['key_concerns'].append("High risk score")
    if state['bankruptcy_flags']:
        state['key_concerns'].append("Bankruptcy indicators present")
    if not state['is_verified']:
        state['key_concerns'].append("Business registration not verified")
    if state.get('years_in_business', 0) < 2:
        state['key_concerns'].append("New business (less than 2 years)")
    
    # Positive factors
    if state['stability_score'] > 0.7:
        state['positive_factors'].append("High stability score")
    if state['growth_indicators']:
        state['positive_factors'].append("Positive growth indicators")
    if state['review_sentiment'] > 0.7:
        state['positive_factors'].append("Excellent online reputation")
    if state.get('years_in_business', 0) > 5:
        state['positive_factors'].append("Well-established business")
    
    state['messages'].append(f"✓ Overall tenant score: {state['overall_tenant_score']:.1f}/100")
    state['messages'].append(f"✓ Recommendation: {state['recommendation']}")
    
    return state

def report_generator_agent(state: TenantResearchState) -> TenantResearchState:
    """Generates comprehensive tenant evaluation report"""
    print("📝 Generating comprehensive report...")
    
    # Calculate confidence level based on data completeness
    data_points = [
        state.get('website_url'),
        state.get('social_media_profiles'),
        state.get('years_in_business'),
        state.get('estimated_revenue'),
        state.get('employee_count'),
        state['is_verified']
    ]
    state['confidence_level'] = sum(1 for dp in data_points if dp) / len(data_points)
    
    # Generate executive summary
    state['executive_summary'] = f"""
TENANT EVALUATION REPORT - {state['company_name']}
{'='*60}

📍 Location: {state['location']}
🏢 Industry: {state.get('industry', 'Not specified')}
📅 Years in Business: {state.get('years_in_business', 'Unknown')}
🏛️ Business Type: {state.get('business_type', 'Unknown')}

OVERALL ASSESSMENT: {state['recommendation']}
Tenant Score: {state['overall_tenant_score']:.1f}/100

KEY METRICS:
• Stability Score: {state['stability_score']:.2f}/1.0
• Growth Potential: {state['growth_potential']:.2f}/1.0
• Risk Score: {state['risk_score']:.2f}/1.0 (lower is better)
• Online Reputation: {state['review_sentiment']:.2f}/1.0

FINANCIAL INDICATORS:
• Estimated Revenue: {state.get('estimated_revenue', 'Not available')}
• Employee Count: {state.get('employee_count', 'Not available')}
• Growth Indicators: {len(state['growth_indicators'])} positive signals

VERIFICATION STATUS:
• Business Registration: {'✓ Verified' if state['is_verified'] else '⚠️ Not Verified'}
• Online Presence: {len(state['social_media_profiles'])} social profiles found
• Current Locations: {len(state['current_locations'])} found

🟢 POSITIVE FACTORS:
{chr(10).join(f'• {factor}' for factor in state['positive_factors']) if state['positive_factors'] else '• No significant positive factors identified'}

🔴 KEY CONCERNS:
{chr(10).join(f'• {concern}' for concern in state['key_concerns']) if state['key_concerns'] else '• No significant concerns identified'}

📊 Data Confidence Level: {state['confidence_level']*100:.0f}%
📚 Data Sources: {len(set(state['data_sources']))} sources consulted
🔍 Searches Performed: {len(state['search_queries_used'])}

RECOMMENDATION RATIONALE:
{_generate_rationale(state)}
"""
    
    state['messages'].append("✓ Report generation complete")
    
    return state

def _generate_rationale(state: TenantResearchState) -> str:
    """Helper function to generate recommendation rationale"""
    if state['recommendation'] == "Highly Recommended":
        return f"""
This tenant demonstrates excellent potential with strong stability indicators
and minimal risk factors. The business appears well-established with positive
growth trajectory and good online reputation.
"""
    elif state['recommendation'] == "Recommended":
        return f"""
This tenant shows good potential with acceptable risk levels. While there may
be some minor concerns, the overall profile suggests a reliable tenant with
reasonable financial stability.
"""
    elif state['recommendation'] == "Proceed with Caution":
        return f"""
This tenant presents moderate risk factors that warrant additional due diligence.
Consider requiring additional financial guarantees or shorter initial lease terms.
Key concerns should be addressed before finalizing any agreements.
"""
    else:
        return f"""
This tenant presents significant risk factors that suggest they may not be
suitable for your property. Multiple red flags were identified during the
research process. Recommend seeking alternative tenants.
"""

# Build the LangGraph workflow
def create_tenant_research_graph():
    builder = StateGraph(TenantResearchState)
    
    # Add all nodes
    builder.add_node("company_identifier", company_identifier_agent)
    builder.add_node("online_presence", online_presence_analyzer)
    builder.add_node("business_verification", business_verification_agent)
    builder.add_node("financial_indicators", financial_indicators_agent)
    builder.add_node("real_estate_history", real_estate_history_agent)
    builder.add_node("risk_assessment", risk_assessment_agent)
    builder.add_node("tenant_scoring", tenant_scoring_agent)
    builder.add_node("report_generator", report_generator_agent)
    
    # Define the flow
    builder.add_edge(START, "company_identifier")
    builder.add_edge("company_identifier", "online_presence")
    builder.add_edge("online_presence", "business_verification")
    builder.add_edge("business_verification", "financial_indicators")
    builder.add_edge("financial_indicators", "real_estate_history")
    builder.add_edge("real_estate_history", "risk_assessment")
    builder.add_edge("risk_assessment", "tenant_scoring")
    builder.add_edge("tenant_scoring", "report_generator")
    builder.add_edge("report_generator", END)
    
    return builder.compile()

# Example usage
if __name__ == "__main__":
    import os
    from IPython.display import Image, display
    
    # Create the research graph
    graph = create_tenant_research_graph()
    
    # Save visualization
    try:
        img = Image(graph.get_graph().draw_mermaid_png())
        with open("faropoint_tenant_research_graph.png", "wb") as f:
            f.write(img.data)
        print("📊 Graph visualization saved!")
    except Exception as e:
        print(f"Visualization error: {e}")
    
    # Print Mermaid diagram
    print("\n🎨 Workflow Diagram:")
    print(graph.get_graph().draw_mermaid())
    
    # Test with example companies
    print("\n" + "="*70)
    print("🏢 FAROPOINT TENANT RESEARCH SYSTEM")
    print("="*70)
    
    # Example small businesses to research
    test_companies = [
        {"name": "Blue Bottle Coffee", "location": "Oakland CA"},
        {"name": "Local Craft Brewery LLC", "location": "San Francisco CA"},
        {"name": "Tech Startup Solutions", "location": "Palo Alto CA"}
    ]
    
    # Only run if API key is set
    if os.getenv("OPENAI_API_KEY"):
        for company in test_companies[:1]:  # Test with first company
            print(f"\n🔍 Researching: {company['name']} - {company['location']}")
            print("-" * 60)
            
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
                "detailed_report": "",
                "key_concerns": [],
                "positive_factors": [],
                "messages": [],
                "data_sources": [],
                "search_queries_used": [],
                "confidence_level": 0.0
            }
            
            try:
                # Run the research workflow
                result = graph.invoke(initial_state)
                
                # Display executive summary
                print(result['executive_summary'])
                
                # Show workflow steps
                print("\n🔄 RESEARCH PROCESS:")
                for msg in result['messages'][-10:]:  # Show last 10 messages
                    print(f"  {msg}")
                    
            except Exception as e:
                print(f"Error: {e}")
                print("Note: This system requires OpenAI API key for LLM analysis")
    else:
        print("\n⚠️ OpenAI API key not found. Set OPENAI_API_KEY environment variable.")
        print("The system uses web search and LLM analysis to research potential tenants.")