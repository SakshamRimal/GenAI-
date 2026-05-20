import streamlit as st
import pandas as pd
from graph.workflow import run_workflow

st.set_page_config(page_title="SQL Agent", page_icon="🤖", layout="wide")
st.title("🤖 Mini SQL Agent")
st.caption("Ask questions about the classicmodels database in plain English.")

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("sql"):
            with st.expander("Generated SQL"):
                st.code(msg["sql"], language="sql")
        if msg.get("dataframe") is not None:
            st.dataframe(msg["dataframe"], use_container_width=True)
        if msg.get("meta"):
            st.caption(msg["meta"])

question = st.chat_input("e.g. How many customers are in France?")

if question:
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            state = run_workflow(question)

        if state.success:
            st.success(state.summary)
            df = pd.DataFrame(state.result) if state.result else pd.DataFrame()
            with st.expander("Generated SQL"):
                st.code(state.sql, language="sql")
            if not df.empty:
                st.dataframe(df, use_container_width=True)
            meta = (
                f"⏱ {state.latency_ms} ms"
                + (f"  |  🔁 {state.retry_count} retries" if state.retry_count else "")
            )
            st.caption(meta)
            st.session_state.messages.append({
                "role": "assistant",
                "content": state.summary,
                "sql": state.sql,
                "dataframe": df,
                "meta": meta,
            })
        else:
            err_msg = f"❌ Failed after {state.retry_count} retries.\n\n**Error:** {state.error}"
            st.error(err_msg)
            with st.expander("Last attempted SQL"):
                st.code(state.sql, language="sql")
            st.session_state.messages.append({
                "role": "assistant",
                "content": err_msg,
                "sql": state.sql,
            })
