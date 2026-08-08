import streamlit as st


def load_css():

    st.markdown("""
<style>

/* ==========================================================
APP
========================================================== */

.stApp{

    background:
    linear-gradient(
        135deg,
        #0B1220,
        #101827,
        #111827
    );

    color:white;

}

/* ==========================================================
SIDEBAR
========================================================== */

section[data-testid="stSidebar"]{

    background:
    linear-gradient(
        180deg,
        #172554,
        #1E293B,
        #111827
    );

    border-right:1px solid rgba(255,255,255,.06);

}

/* ==========================================================
HEADINGS
========================================================== */

h1{

    font-weight:800;

    color:white;

}

h2,h3{

    color:white;

}

/* ==========================================================
CAPTION
========================================================== */

[data-testid="stCaptionContainer"]{

    color:#CBD5E1;

}

/* ==========================================================
CHAT MESSAGE
========================================================== */

[data-testid="stChatMessage"]{

    background:rgba(255,255,255,.05);

    border-radius:20px;

    padding:20px;

    border:1px solid rgba(255,255,255,.08);

    margin-bottom:18px;

}

/* ==========================================================
METRIC
========================================================== */

[data-testid="metric-container"]{

    background:rgba(255,255,255,.05);

    border-radius:18px;

    border:1px solid rgba(255,255,255,.08);

    padding:15px;

}

/* ==========================================================
SELECT BOX
========================================================== */

.stSelectbox{

    margin-bottom:10px;

}

/* ==========================================================
BUTTON
========================================================== */

.stButton>button{

    width:100%;

    background:
    linear-gradient(
        90deg,
        #2563EB,
        #7C3AED
    );

    color:white;

    border:none;

    border-radius:12px;

    font-weight:700;

    transition:.25s;

}

.stButton>button:hover{

    transform:translateY(-2px);

}

/* ==========================================================
INFO BOX
========================================================== */

div[data-testid="stAlert"]{

    border-radius:16px;

}

/* ==========================================================
CHAT INPUT
========================================================== */

[data-testid="stChatInput"]{

    background:rgba(255,255,255,.05);

    border-radius:20px;

}

/* ==========================================================
SCROLLBAR
========================================================== */

::-webkit-scrollbar{

    width:8px;

}

::-webkit-scrollbar-thumb{

    background:#334155;

    border-radius:20px;

}

/* ==========================================================
HIDE STREAMLIT
========================================================== */

#MainMenu{

    visibility:hidden;

}

footer{

    visibility:hidden;

}

</style>
""",
    unsafe_allow_html=True
    )