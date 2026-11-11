import streamlit as st
from generation import classify_ticket, generate_email_draft

st.set_page_config(page_title="AI Ticket Triage", layout="wide")

st.title("AI Support Ticket Triage Dashboard")
st.markdown("Automated ticket classification, priority routing, and draft response generation.")

st.sidebar.header("Settings & Info")
st.sidebar.info("Model: **gemini-3.5-flash-lite**\n\nModular Architecture: Reusing `app.py` backend logic.")

sample_tickets = {
    "Custom Input": "",
    "System Error (Urgent)": "URGENT: Our production checkout page is returning 500 server errors!",
    "Support Inquiry": "Hi, I forgot my password and the reset link is not working.",
    "Feature Request": "Could you add an export to PDF feature in the analytics tab?",
    "Spam Message": "Cheapest SEO packages guaranteed boost your ranking today!"
}

selected_option = st.selectbox("Select a Sample Ticket or enter your own:", list(sample_tickets.keys()))
default_text = sample_tickets[selected_option] if selected_option != "Custom Input" else ""

customer_input = st.text_area(
    "Incoming Customer Message / Ticket:",
    value=default_text,
    height=140,
    placeholder="Type or paste a customer message here..."
)

if st.button("Process Ticket", type="primary"):
    if not customer_input.strip():
        st.warning("Please enter a customer message first.")
    else:
        with st.spinner("Analyzing ticket with Gemin..."):
            result = classify_ticket(customer_input)

            st.divider()
            col1, col2 = st.columns([1, 1])

            with col1:
                st.subheader("Structured Classification")
                category = result.get("category", "UNKNOWN")
                priority = result.get("priority", "LOW")

                st.metric(label="Category", value=category)
                st.metric(label="Priority Level", value=priority)

                st.markdown("**Summary:**")
                st.info(result.get("summary", "N/A"))

                with st.expander("View Raw JSON Output"):
                    st.json(result)

            with col2:
                st.subheader("Automated Action & Draft")

                if category in ["SUPPORT", "FEATURE_REQUEST"]:
                    with st.spinner("Generating response draft..."):
                        draft = generate_email_draft(customer_input, result.get("summary", ""))
                        st.success("Draft Response Generated")
                        st.text_area("Generated Email Reply:", value=draft, height=220)
                elif category == "URGENT":
                    st.error("ESCALATION REQUIRED: Ticket added to high-priority urgent alert queue.")
                    st.json({
                        "status": "Escalated",
                        "alert_target": "On-call Engineering Team",
                        "summary": result.get("summary")
                    })
                elif category == "SPAM":
                    st.warning("SPAM DETECTED: Message filtered and logged to audit trail.")
                    st.json({
                        "status": "Ignored",
                        "action": "Logged to audit_trail.csv"
                    })