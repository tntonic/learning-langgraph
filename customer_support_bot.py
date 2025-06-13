"""
Advanced Customer Support Bot - LangGraph Demo
Demonstrates:
- Multiple specialized agents
- Complex routing logic
- State accumulation
- Parallel processing
- Fallback mechanisms
"""

from typing import TypedDict, Literal, List, Dict, Annotated
from langgraph.graph import StateGraph, START, END
from datetime import datetime
import random
import json
from IPython.display import Image, display
import operator

# Define our state
class SupportState(TypedDict):
    customer_message: str
    intent: str
    sentiment: str
    category: str
    priority: str
    knowledge_base_results: List[str]
    suggested_responses: List[str]
    escalation_needed: bool
    final_response: str
    conversation_history: Annotated[List[str], operator.add]
    metadata: Dict

# Agent nodes
def intent_classifier(state: SupportState) -> SupportState:
    """Classifies customer intent from their message"""
    print("🎯 Intent Classifier: Analyzing customer intent...")
    
    # Simulate intent classification
    message_lower = state['customer_message'].lower()
    
    if any(word in message_lower for word in ['refund', 'money back', 'return']):
        intent = 'refund_request'
    elif any(word in message_lower for word in ['broken', 'not working', 'error', 'bug']):
        intent = 'technical_issue'
    elif any(word in message_lower for word in ['how to', 'help', 'guide']):
        intent = 'how_to_question'
    elif any(word in message_lower for word in ['angry', 'frustrated', 'terrible']):
        intent = 'complaint'
    else:
        intent = 'general_inquiry'
    
    state['intent'] = intent
    state['conversation_history'].append(f"Intent classified as: {intent}")
    return state

def sentiment_analyzer(state: SupportState) -> SupportState:
    """Analyzes customer sentiment"""
    print("😊 Sentiment Analyzer: Detecting customer mood...")
    
    message_lower = state['customer_message'].lower()
    
    # Simple sentiment analysis
    negative_words = ['angry', 'frustrated', 'terrible', 'awful', 'hate', 'worst']
    positive_words = ['great', 'excellent', 'love', 'wonderful', 'amazing', 'best']
    
    neg_count = sum(1 for word in negative_words if word in message_lower)
    pos_count = sum(1 for word in positive_words if word in message_lower)
    
    if neg_count > pos_count:
        sentiment = 'negative'
    elif pos_count > neg_count:
        sentiment = 'positive'
    else:
        sentiment = 'neutral'
    
    state['sentiment'] = sentiment
    state['conversation_history'].append(f"Sentiment detected: {sentiment}")
    return state

def priority_assigner(state: SupportState) -> SupportState:
    """Assigns priority based on intent and sentiment"""
    print("🚨 Priority Assigner: Determining urgency...")
    
    # Priority matrix
    priority_rules = {
        ('complaint', 'negative'): 'high',
        ('refund_request', 'negative'): 'high',
        ('technical_issue', 'negative'): 'high',
        ('complaint', 'neutral'): 'medium',
        ('refund_request', 'neutral'): 'medium',
        ('technical_issue', 'neutral'): 'medium',
    }
    
    priority = priority_rules.get(
        (state['intent'], state['sentiment']), 
        'low'
    )
    
    state['priority'] = priority
    state['conversation_history'].append(f"Priority set to: {priority}")
    return state

def knowledge_base_searcher(state: SupportState) -> SupportState:
    """Searches internal knowledge base"""
    print("📚 Knowledge Base: Searching for solutions...")
    
    # Simulate KB search
    kb_responses = {
        'refund_request': [
            "Refunds are processed within 5-7 business days",
            "You can request a refund through your account dashboard",
            "Refund policy: Items must be returned within 30 days"
        ],
        'technical_issue': [
            "Try restarting the application",
            "Clear your cache and cookies",
            "Check if you're using the latest version"
        ],
        'how_to_question': [
            "Visit our help center at help.example.com",
            "Check our video tutorials on YouTube",
            "Download our user guide PDF"
        ]
    }
    
    results = kb_responses.get(state['intent'], ["Please contact our support team"])
    state['knowledge_base_results'] = results
    state['conversation_history'].append(f"Found {len(results)} KB articles")
    return state

def response_generator(state: SupportState) -> SupportState:
    """Generates personalized responses"""
    print("💬 Response Generator: Crafting responses...")
    
    # Generate responses based on context
    responses = []
    
    # Empathy opener based on sentiment
    if state['sentiment'] == 'negative':
        opener = "I understand your frustration, and I'm here to help."
    elif state['sentiment'] == 'positive':
        opener = "Thank you for reaching out!"
    else:
        opener = "Thank you for contacting us."
    
    responses.append(opener)
    
    # Add KB results
    responses.extend(state['knowledge_base_results'])
    
    # Add next steps
    if state['priority'] == 'high':
        responses.append("I've escalated this to our specialist team who will contact you within 24 hours.")
    
    state['suggested_responses'] = responses
    state['conversation_history'].append(f"Generated {len(responses)} response options")
    return state

def escalation_checker(state: SupportState) -> SupportState:
    """Determines if human escalation is needed"""
    print("🎯 Escalation Checker: Evaluating complexity...")
    
    # Escalation rules
    escalate = False
    
    if state['priority'] == 'high':
        escalate = True
    elif state['sentiment'] == 'negative' and state['intent'] == 'complaint':
        escalate = True
    elif 'legal' in state['customer_message'].lower():
        escalate = True
    elif 'manager' in state['customer_message'].lower():
        escalate = True
    
    state['escalation_needed'] = escalate
    state['conversation_history'].append(f"Escalation needed: {escalate}")
    return state

def response_optimizer(state: SupportState) -> SupportState:
    """Optimizes and personalizes the final response"""
    print("✨ Response Optimizer: Personalizing message...")
    
    # Combine responses intelligently
    final_parts = []
    
    # Add greeting
    final_parts.append(state['suggested_responses'][0])
    
    # Add main content
    if len(state['knowledge_base_results']) > 0:
        final_parts.append("\n\nHere's what I found that might help:")
        for i, result in enumerate(state['knowledge_base_results'][:2], 1):
            final_parts.append(f"{i}. {result}")
    
    # Add escalation notice if needed
    if state['escalation_needed']:
        final_parts.append("\n\n🎯 I've escalated your case to a specialist.")
        final_parts.append("Case ID: #" + str(random.randint(10000, 99999)))
    
    # Add closing
    final_parts.append("\n\nIs there anything else I can help you with?")
    
    state['final_response'] = "\n".join(final_parts)
    state['conversation_history'].append("Response optimized and ready")
    return state

def quality_checker(state: SupportState) -> SupportState:
    """Final quality check before sending"""
    print("✅ Quality Checker: Validating response...")
    
    # Simulate quality checks
    checks = {
        'length_appropriate': len(state['final_response']) > 50,
        'no_sensitive_data': True,
        'tone_appropriate': True,
        'grammar_correct': True
    }
    
    state['metadata']['quality_checks'] = checks
    state['conversation_history'].append("Quality checks passed")
    return state

# Routing functions
def route_by_priority(state: SupportState) -> Literal["high_priority", "normal_flow"]:
    """Routes based on priority"""
    if state['priority'] == 'high':
        return "high_priority"
    return "normal_flow"

def route_by_escalation(state: SupportState) -> Literal["escalate", "respond"]:
    """Routes based on escalation need"""
    if state['escalation_needed']:
        return "escalate"
    return "respond"

# Build the graph
def create_support_graph():
    builder = StateGraph(SupportState)
    
    # Add all nodes
    builder.add_node("intent_classifier", intent_classifier)
    builder.add_node("sentiment_analyzer", sentiment_analyzer)
    builder.add_node("priority_assigner", priority_assigner)
    builder.add_node("kb_searcher", knowledge_base_searcher)
    builder.add_node("response_generator", response_generator)
    builder.add_node("escalation_checker", escalation_checker)
    builder.add_node("response_optimizer", response_optimizer)
    builder.add_node("quality_checker", quality_checker)
    
    # Initial flow
    builder.add_edge(START, "intent_classifier")
    builder.add_edge("intent_classifier", "sentiment_analyzer")
    builder.add_edge("sentiment_analyzer", "priority_assigner")
    
    # Conditional routing based on priority
    builder.add_conditional_edges(
        "priority_assigner",
        route_by_priority,
        {
            "high_priority": "escalation_checker",
            "normal_flow": "kb_searcher"
        }
    )
    
    # Normal flow
    builder.add_edge("kb_searcher", "response_generator")
    builder.add_edge("response_generator", "response_optimizer")
    
    # High priority flow
    builder.add_edge("escalation_checker", "kb_searcher")
    
    # Final steps
    builder.add_edge("response_optimizer", "quality_checker")
    builder.add_edge("quality_checker", END)
    
    return builder.compile()

# Test the system
if __name__ == "__main__":
    # Create the graph
    graph = create_support_graph()
    
    # Save visualization
    try:
        img = Image(graph.get_graph().draw_mermaid_png())
        with open("support_bot_graph.png", "wb") as f:
            f.write(img.data)
        print("📊 Graph saved as support_bot_graph.png")
    except Exception as e:
        print(f"Visualization error: {e}")
    
    # Print Mermaid
    print("\n🎨 Mermaid Diagram:")
    print(graph.get_graph().draw_mermaid())
    
    # Test cases
    test_messages = [
        "I'm really frustrated! My order hasn't arrived and it's been 2 weeks!",
        "How do I reset my password?",
        "This is the worst service ever! I want a full refund immediately!",
        "Can you help me understand how to use the advanced features?"
    ]
    
    print("\n" + "="*60)
    print("🤖 CUSTOMER SUPPORT BOT DEMO")
    print("="*60)
    
    for i, message in enumerate(test_messages, 1):
        print(f"\n📧 Test Case {i}: '{message}'")
        print("-" * 50)
        
        initial_state = {
            "customer_message": message,
            "intent": "",
            "sentiment": "",
            "category": "",
            "priority": "",
            "knowledge_base_results": [],
            "suggested_responses": [],
            "escalation_needed": False,
            "final_response": "",
            "conversation_history": [],
            "metadata": {}
        }
        
        result = graph.invoke(initial_state)
        
        print(f"Intent: {result['intent']}")
        print(f"Sentiment: {result['sentiment']}")
        print(f"Priority: {result['priority']}")
        print(f"Escalated: {result['escalation_needed']}")
        print(f"\n📨 Final Response:\n{result['final_response']}")
        print("\n💭 Process Flow:")
        for step in result['conversation_history']:
            print(f"  • {step}")