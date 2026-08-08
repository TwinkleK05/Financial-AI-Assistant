import streamlit as st

from api_client import (
    ask_question,
    health,
    send_feedback,
)

from styles import load_css

from components import (
    page_header,
    welcome,
    sidebar_stats,
    backend_status,
    source_card,
    feedback_buttons,
)

# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="Financial AI Assistant",
    layout="wide",
    initial_sidebar_state="expanded",
)

load_css()

# ==================================================
# SESSION STATE
# ==================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

# ==================================================
# SIDEBAR
# ==================================================

with st.sidebar:

    st.title("Financial AI")

    st.caption(
        "Enterprise Knowledge Assistant"
    )

    st.divider()

    role = st.selectbox(
        "User Role",
        [
            "CEO",
            "Finance",
            "CTO",
            "Intern",
        ],
    )

    st.divider()

    sidebar_stats()

    st.divider()

    try:

        result = health()

        backend_status(
            result["status"] == "ok"
        )

    except:

        backend_status(False)

# ==================================================
# HEADER
# ==================================================

page_header()

# ==================================================
# EMPTY CHAT
# ==================================================

if len(st.session_state.messages) == 0:

    welcome()

# ==================================================
# CHAT HISTORY
# ==================================================

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )

        if (
            message["role"] == "assistant"
            and "sources" in message
        ):

            st.markdown("---")

            st.subheader("Sources")

            for source in message["sources"]:

                source_card(source)

# ==================================================
# USER INPUT
# ==================================================

question = st.chat_input(
    "Ask anything about your financial documents..."
)

# ==================================================
# ASK
# ==================================================

if question:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question,
        }
    )

    with st.chat_message("user"):

        st.markdown(question)

    with st.chat_message("assistant"):

        with st.spinner(
            "Searching knowledge base..."
        ):

            try:

                response = ask_question(
                    question=question,
                    role=role,
                )

                answer = response["answer"]

                sources = response["sources"]

                st.markdown(answer)

                if sources:

                    st.markdown("---")

                    st.subheader(
                        "Sources"
                    )

                    for source in sources:

                        source_card(source)

                helpful, not_helpful = feedback_buttons(
                    question
                )

                if helpful:

                    send_feedback(
                        question,
                        rating=5,
                        comment="Helpful",
                    )

                    st.toast(
                        "Feedback submitted!"
                    )

                if not_helpful:

                    send_feedback(
                        question,
                        rating=1,
                        comment="Not Helpful",
                    )

                    st.toast(
                        "Feedback submitted!"
                    )

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer,
                        "sources": sources,
                    }
                )

            except Exception as error:

                st.error(str(error))