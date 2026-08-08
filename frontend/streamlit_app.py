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
#
# Everything (answers, sources and feedback controls) is rendered
# from session history. Rendering feedback here — rather than only on
# the run that produced the answer — is what makes the buttons work:
# clicking one triggers a rerun in which the question box is empty,
# so a submit-time-only handler would never fire.

for index, message in enumerate(st.session_state.messages):

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )

        if message["role"] == "assistant":

            if message.get("sources"):

                st.markdown("---")

                st.subheader("Sources")

                for source in message["sources"]:

                    source_card(source)

            # ------------------------------------------
            # Feedback loop entry point
            # ------------------------------------------

            submitted_key = f"feedback_submitted_{index}"

            helpful, not_helpful = feedback_buttons(
                key=index,
                submitted=st.session_state.get(submitted_key, False),
            )

            if helpful or not_helpful:

                try:

                    send_feedback(
                        question=message.get("question", ""),
                        rating=5 if helpful else 1,
                        comment="Helpful" if helpful else "Not Helpful",
                        chunk_ids=message.get("chunk_ids"),
                    )

                    st.session_state[submitted_key] = True

                    st.toast("Feedback submitted!")

                    st.rerun()

                except Exception as error:

                    st.error(str(error))

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

    try:

        with st.spinner("Searching knowledge base..."):

            response = ask_question(
                question=question,
                role=role,
            )

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": response["answer"],
                "sources": response.get("sources", []),
                "chunk_ids": response.get("chunk_ids", []),
                "question": question,
            }
        )

    except Exception as error:

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": f"⚠️ {error}",
            }
        )

    # Re-run so the new turn (and its working feedback controls)
    # render through the history loop above.
    st.rerun()