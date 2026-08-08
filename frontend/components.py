import streamlit as st


# ==================================================
# PAGE HEADER
# ==================================================

def page_header():

    st.markdown(
        """
<div class="card">

<h1 class="main-title">
 Financial AI Assistant
</h1>

<p class="sub-title">
Enterprise RAG Assistant powered by
FAISS • Groq • SQLite • FastAPI
</p>

</div>
""",
        unsafe_allow_html=True,
    )


# ==================================================
# WELCOME
# ==================================================
def welcome():

    st.markdown(
        """
<div style="text-align:center;padding:70px 20px;">

<h1 style="
font-size:42px;
font-weight:800;
color:white;
">

Financial AI Assistant

</h1>

<p style="
font-size:18px;
color:#CBD5E1;
">

Enterprise Retrieval-Augmented Generation Assistant

</p>

<br>

<div style="
background:#1E293B;
padding:25px;
border-radius:20px;
max-width:700px;
margin:auto;
border:1px solid rgba(255,255,255,.08);
">

### Try asking

• What is Apple's market cap?

• Compare Apple and Google.

• Show Microsoft's PE Ratio.

• Explain EBITDA.

• Which company has the highest revenue?

</div>

</div>
""",
        unsafe_allow_html=True,
    )


# ==================================================
# SOURCE CARD
# ==================================================
def source_card(source):

    sheet = source["sheet"] if source["sheet"] else "—"
    page = source["page"] if source["page"] else "—"
    row = source["row"] if source["row"] else "—"

    st.markdown(
        f"""
<div style="
background:linear-gradient(135deg,#1e293b,#111827);
padding:18px;
border-radius:16px;
border:1px solid rgba(255,255,255,.08);
margin-bottom:15px;
box-shadow:0 4px 15px rgba(0,0,0,.25);
">

<div style="
font-size:18px;
font-weight:700;
color:white;
margin-bottom:15px;
">

 {source["source"]}

</div>

<div style="
display:flex;
gap:12px;
flex-wrap:wrap;
">

<div style="
background:#2563EB;
padding:6px 12px;
border-radius:20px;
color:white;
font-size:13px;
">

🔒 {source["access"].title()}

</div>

<div style="
background:#334155;
padding:6px 12px;
border-radius:20px;
color:white;
font-size:13px;
">

 Sheet: {sheet}

</div>

<div style="
background:#334155;
padding:6px 12px;
border-radius:20px;
color:white;
font-size:13px;
">

📍 Row: {row}

</div>

<div style="
background:#334155;
padding:6px 12px;
border-radius:20px;
color:white;
font-size:13px;
">

 Page: {page}

</div>

</div>

</div>
""",
        unsafe_allow_html=True,
    )

# ==================================================
# SIDEBAR
# ==================================================

def sidebar_stats():

    st.subheader("Knowledge Base")

    c1, c2 = st.columns(2)

    with c1:

        st.metric(
            "Docs",
            "534"
        )

    with c2:

        st.metric(
            "Chunks",
            "889"
        )


# ==================================================
# BACKEND STATUS
# ==================================================

def backend_status(online: bool):

    if online:

        st.success(
            "🟢 Backend Connected"
        )

    else:

        st.error(
            "🔴 Backend Offline"
        )


# ==================================================
# FEEDBACK
# ==================================================

def feedback_buttons(key, submitted=False):
    """
    Render thumbs up/down controls for one answer.

    `key` must be stable and unique per answer (e.g. the message index)
    so the buttons keep working across Streamlit reruns. Once feedback
    has been submitted a confirmation is shown instead.

    Returns (helpful, not_helpful) booleans.
    """

    if submitted:

        st.caption("✅ Thanks for your feedback!")

        return False, False

    c1, c2 = st.columns(2)

    with c1:

        helpful = st.button(
            "👍 Helpful",
            use_container_width=True,
            key=f"help_{key}",
        )

    with c2:

        not_helpful = st.button(
            "👎 Not Helpful",
            use_container_width=True,
            key=f"not_help_{key}",
        )

    return helpful, not_helpful