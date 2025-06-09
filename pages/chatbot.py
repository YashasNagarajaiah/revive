import streamlit as st
import pandas as pd
import random
from datetime import datetime
from config import FILE_PATH, EMISSION_FACTORS
from pages.chatbot_handlers import (
    handle_total_weight,
    handle_composition,
    handle_collections,
    handle_environmental,
    handle_monthly,
    get_help_message
)

# Configuration for Zain's responses
CHATBOT_RESPONSES = {
    "greeting": [
        "Hi there! I'm Zain, your waste management assistant. How can I help you today?",
        "Hello! I'm Zain, ready to help you analyze your waste management data!",
        "Hey! This is Zain, here to assist with your waste analytics. What would you like to know?"
    ],
    "farewell": [
        "Goodbye! Feel free to come back when you need more analysis. -Zain",
        "See you later! Don't hesitate to ask if you need more data insights. -Zain",
        "Take care! I'm here whenever you need help understanding your waste metrics. -Zain"
    ],
    "confusion": [
        "I'm not quite sure I understood that. Could you rephrase your question? -Zain",
        "I might need more clarity on that. Could you ask in a different way? -Zain",
        "I'm still learning! Could you try asking that question differently? -Zain"
    ]
}

def initialize_session_state():
    """Initialize session state for chat history"""
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

def calculate_detailed_metrics(df):
    """Calculate comprehensive metrics with detailed breakdowns"""
    try:
        # Basic metrics
        metrics = {
            "total_weight": df["Weight (Kg)"].sum(),
            "total_collections": df["IS Number"].nunique(),
            "dates": {
                "latest": df["Incoming Date"].max(),
                "earliest": df["Incoming Date"].min()
            }
        }
        
        # Monthly calculations
        df['Month'] = pd.to_datetime(df['Incoming Date']).dt.strftime('%Y-%m')
        current_month = df['Month'].max()
        prev_month = df[df['Month'] != current_month]['Month'].max()
        
        # Monthly metrics
        metrics["monthly"] = {
            "current": {
                "month": current_month,
                "weight": df[df['Month'] == current_month]['Weight (Kg)'].sum(),
                "collections": df[df['Month'] == current_month]['IS Number'].nunique()
            },
            "previous": {
                "month": prev_month,
                "weight": df[df['Month'] == prev_month]['Weight (Kg)'].sum(),
                "collections": df[df['Month'] == prev_month]['IS Number'].nunique()
            }
        }
        
        # Calculate growth rates
        if metrics["monthly"]["previous"]["weight"] > 0:
            metrics["growth"] = {
                "weight": ((metrics["monthly"]["current"]["weight"] - metrics["monthly"]["previous"]["weight"]) 
                          / metrics["monthly"]["previous"]["weight"] * 100),
                "collections": ((metrics["monthly"]["current"]["collections"] - metrics["monthly"]["previous"]["collections"]) 
                              / metrics["monthly"]["previous"]["collections"] * 100)
            }
        else:
            metrics["growth"] = {"weight": 0, "collections": 0}
        
        # Waste composition analysis
        composition = df.groupby("Waste Streams")["Weight (Kg)"].agg([
            'sum', 'count', 'mean'
        ]).round(2).reset_index()
        composition['percentage'] = (composition['sum'] / metrics['total_weight'] * 100).round(2)
        composition = composition.sort_values('sum', ascending=False)
        
        metrics["composition"] = {
            row['Waste Streams']: {
                'total_weight': row['sum'],
                'collections': row['count'],
                'average_weight': row['mean'],
                'percentage': row['percentage']
            } for _, row in composition.iterrows()
        }
        
        # Environmental impact calculations
        total_co2 = sum((metrics["composition"][stream]['total_weight'] / 1000) * 
                       EMISSION_FACTORS.get(stream, 2.5) for stream in metrics["composition"])
        
        metrics["environmental"] = {
            "co2_prevented": total_co2,
            "carbon_reduced": total_co2 / 3.67,
            "trees_equivalent": total_co2 * 0.0164,
            "by_stream": {
                stream: {
                    "co2": (data['total_weight'] / 1000) * EMISSION_FACTORS.get(stream, 2.5)
                } for stream, data in metrics["composition"].items()
            }
        }
        
        return metrics
    except Exception as e:
        st.error(f"Error calculating metrics: {str(e)}")
        return {}

def get_response(user_input, df):
    """Generate detailed responses based on user input and calculated metrics"""
    try:
        user_input = user_input.lower().strip()
        
        # Handle greetings and farewells
        if any(word in user_input for word in ["hi", "hello", "hey"]):
            return random.choice(CHATBOT_RESPONSES["greeting"])
        if any(word in user_input for word in ["bye", "goodbye", "see you"]):
            return random.choice(CHATBOT_RESPONSES["farewell"])
        
        # Check if data is available
        if df is None or df.empty:
            return "I don't have any data to analyze at the moment. Please ensure your data is loaded."
        
        # Calculate metrics once for all queries
        metrics = calculate_detailed_metrics(df)
        
        # Query patterns dictionary
        query_patterns = {
            # Total waste collection patterns
            "total waste collection": lambda: handle_total_weight(metrics),
            "total weight": lambda: handle_total_weight(metrics),
            "waste collected": lambda: handle_total_weight(metrics),
            "how much waste": lambda: handle_total_weight(metrics),
            
            # Composition patterns
            "composition breakdown": lambda: handle_composition(metrics),
            "waste stream": lambda: handle_composition(metrics),
            "waste composition": lambda: handle_composition(metrics),
            "waste type": lambda: handle_composition(metrics),
            
            # Collection patterns
            "how many collection": lambda: handle_collections(metrics),
            "total collection": lambda: handle_collections(metrics),
            "number of collection": lambda: handle_collections(metrics),
            
            # Environmental impact patterns
            "environmental impact": lambda: handle_environmental(metrics),
            "carbon footprint": lambda: handle_environmental(metrics),
            "environmental saving": lambda: handle_environmental(metrics),
            
            # Monthly performance patterns
            "monthly performance": lambda: handle_monthly(metrics),
            "this month": lambda: handle_monthly(metrics),
            "month comparison": lambda: handle_monthly(metrics),
            "how did i perform": lambda: handle_monthly(metrics)
        }
        
        # Check for pattern matches
        for pattern, handler in query_patterns.items():
            if pattern in user_input:
                return handler()
        
        # Handle help requests
        if "help" in user_input or "what can you" in user_input:
            return get_help_message()
        
        return random.choice(CHATBOT_RESPONSES["confusion"])
        
    except Exception as e:
        return f"I encountered an error while processing your request: {str(e)}"

def display_chatbot_page():
    """Display the chatbot interface"""
    st.title("Zain - Your Waste Management Assistant")
    
    # Initialize session state
    initialize_session_state()
    
    # Load user data if logged in
    if 'username' in st.session_state:
        try:
            df_outgoing = pd.read_excel(FILE_PATH, sheet_name='Outgoing')
            if 'Source' not in df_outgoing.columns:
                st.error("Data format error: 'Source' column not found")
                return
                
            user_df = df_outgoing[df_outgoing['Source'] == st.session_state['username']].copy()
            if user_df.empty:
                st.warning(f"No data found for user {st.session_state['username']}")
                return
                
            user_df['Incoming Date'] = pd.to_datetime(user_df['Incoming Date'])
            
        except Exception as e:
            st.error(f"Error loading data: {str(e)}")
            return
    else:
        st.warning("Please log in to chat with Zain.")
        return

    # Display help and suggestions
    with st.expander("How can Zain help you?", expanded=False):
        st.write("""
        I can help you with:
        
        Collection Analysis:
        - Total waste collection data
        - Waste composition breakdown
        - Collection statistics and trends
        
        Environmental Impact:
        - Carbon footprint analysis
        - Environmental savings
        - Sustainability metrics
        
        Performance Metrics:
        - Monthly comparisons
        - Growth analysis
        - Efficiency indicators
        
        Try asking questions like:
        - What is my total waste collection?
        - Show me waste composition breakdown
        - How many collections have I made?
        - What's my environmental impact?
        - How did I perform this month?
        """)

    # Display chat history
    for user_msg, bot_msg in st.session_state.chat_history:
        with st.chat_message("user"):
            st.write(user_msg)
        with st.chat_message("assistant"):
            st.write(bot_msg)

    # Chat input and response handling
    user_input = st.chat_input("Ask Zain a question...")
    
    if user_input:
        # Show user message
        with st.chat_message("user"):
            st.write(user_input)
        
        # Generate response
        try:
            response = get_response(user_input, user_df)
            
            # Show assistant response
            with st.chat_message("assistant"):
                st.write(response)
            
            # Update chat history
            st.session_state.chat_history.append((user_input, response))
            
        except Exception as e:
            error_msg = f"Sorry, this is Zain. I encountered an error: {str(e)}"
            with st.chat_message("assistant"):
                st.error(error_msg)
            st.session_state.chat_history.append((user_input, error_msg))