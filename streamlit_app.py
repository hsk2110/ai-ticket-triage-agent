import streamlit as st
from generation import classify_ticket, generate_email_draft

st.set_page_config(page_title="RAG AI Ticket Triage", layout="wide")

st.title("RAG-Grounded AI Ticket Triage Dashboard")
st.caption("Powered by Google Gemini Flash-Lite & ChromaDB Local Vector Search")

sample_tickets = {
    "Custom Input": "",
    "Invoice Request": "Hi, where can I download my invoice for September?",
    "Password Issue": "I requested a password reset link but didn't receive an email.",
    "Database Error": "URGENT: Our production database is returning 500 errors!",
    "Feature Suggestion": "Could you add dark mode to the dashboard?"
}

selected_option = st.selectbox("Select a Sample Ticket:", list(sample_tickets.keys()))
default_text = sample_tickets[selected_option] if selected_option != "Custom Input" else ""

customer_input = st.text_area("Incoming Customer Message:", value=default_text, height=130)

if st.button("Process Ticket with RAG", type="primary"):
    if not customer_input.strip():
        st.warning("Please enter a customer message.")
    else:
        with st.spinner("Classifying & Searching Vector Database..."):
            result = classify_ticket(customer_input)
            category = result.get("category", "UNKNOWN")
            
            st.divider()
            col1, col2 = st.columns([1, 1])

            with col1:
                st.subheader("Classification")
                st.metric("Category", category)
                st.metric("Priority", result.get("priority", "LOW"))
                st.info(result.get("summary", ""))

            with col2:
                st.subheader("⚡ Grounded Response & RAG Context")
                
                if category in ["SUPPORT", "FEATURE_REQUEST"]:
                    draft, context = generate_email_draft(customer_input, result.get("summary", ""))
                    
                    st.success("Draft Response Generated")
                    st.text_area("Generated Email Reply:", value=draft, height=200)
                    
                    with st.expander("View Retrieved ChromaDB Context (RAG Evidence)"):
                        st.code(context, language="markdown")

                elif category == "URGENT":
                    st.error("ESCALATION REQUIRED: Production issue flagged.")
                elif category == "SPAM":
                    st.warning("SPAM: Filtered and logged.")