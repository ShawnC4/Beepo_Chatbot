import streamlit as st
import streamlit.components.v1 as components

# Set up the Streamlit page
st.set_page_config(
    page_title="Tastybox Bites Chatbot",
    page_icon="🍔",
    layout="wide"
)

# Restaurant Menu Data
menu = {
    "Mains": [
        {"name": "Laksa", "price": "$5.00"},
        {"name": "Braised Duck Rice", "price": "$4.50"},
        {"name": "Nasi Lemak", "price": "$6.00"},
        {"name": "Mala", "price": "$12.00"},
        {"name": "Burrito", "price": "$7.00"},
        {"name": "Ban Mian", "price": "$5.50"},
        {"name": "Pork Leg Rice", "price": "$5.50"},
    ],
    "Drinks": [
        {"name": "Mango Smoothie", "price": "$4.00"},
        {"name": "Passion Fruit Tea", "price": "$3.00"},
    ],
}

# Function to display the menu
def display_menu():
    st.markdown("""
        <style>
        .menu-container {
            padding: 20px;
            font-size: 1.2rem;
        }
        .menu-category {
            margin-bottom: 20px;
        }
        .menu-category h3 {
            font-size: 1.5rem;
            margin-bottom: 10px;
        }
        .menu-category p {
            font-size: 1rem;
            margin: 5px 0;
        }
        /* Chatbot Styling */
        df-messenger {
            position: fixed;
            bottom: 10px;
            right: 10px;
            z-index: 999;
            --df-messenger-font-color: #000;
            --df-messenger-font-family: Google Sans;
            --df-messenger-chat-background: #f3f6fc;
            --df-messenger-message-user-background: #d3e3fd;
            --df-messenger-message-bot-background: #fff;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Display Menu
    st.header("🍽️ Tastybox Bites Menu")
    for category, items in menu.items():
        st.subheader(category)
        for item in items:
            st.write(f"**{item['name']}** - {item['price']}")

# Create two columns side by side
col1, col2 = st.columns([1, 1])

# Display the menu on the left side
with col1:
    display_menu()
    st.markdown("---")
    st.write("💬 Chat with Tastybox Bites's assistant, BEEPO, to place or track order")

# Embed the Dialogflow CX Chatbot on the right side
with col2:


    # Embed the Dialogflow CX Chatbot (HTML iframe for Dialogflow)
    df_chatbot_code = """
    <link rel="stylesheet" href="https://www.gstatic.com/dialogflow-console/fast/df-messenger/prod/v1/themes/df-messenger-default.css">
    <script src="https://www.gstatic.com/dialogflow-console/fast/df-messenger/prod/v1/df-messenger.js"></script>
    <df-messenger
    location="asia-southeast1"
    project-id="beepochatbot"
    agent-id="dc1d9410-dc19-4b8a-ac1d-6c925baf2dab"
    language-code="en"
    max-query-length="-1">
    <df-messenger-chat-bubble
    chat-title="Beepo">
    </df-messenger-chat-bubble>
    </df-messenger>
    <style>
    df-messenger {
        z-index: 999;
        position: fixed;
        --df-messenger-font-color: #000;
        --df-messenger-font-family: Google Sans;
        --df-messenger-chat-background: #f3f6fc;
        --df-messenger-message-user-background: #d3e3fd;
        --df-messenger-message-bot-background: #fff;
        bottom: 10px;
        right: 10px;
    }
    </style>
    """
    components.html(df_chatbot_code, height=700)

