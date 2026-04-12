import streamlit as st
from agent.sql_gen import load_data, generate_sql, run_query, fix_sql
from agent.insight import generate_insight
from agent.chart import auto_chart

st.set_page_config(page_title="Data Q&A Agent", page_icon="📊", layout="wide")

st.title("📊 Data Q&A Agent")
st.caption("Ask any question about the Olist e-commerce database in plain English.")

@st.cache_resource
def init_db():
    load_data()

init_db()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])
        if "chart" in message and message["chart"] is not None:
            st.plotly_chart(message["chart"], use_container_width=True)
        if "sql" in message:
            with st.expander("See SQL query"):
                st.code(message["sql"], language="sql")

question = st.chat_input("Ask a question about the data...")

if question:
    with st.chat_message("user"):
        st.write(question)
    st.session_state.messages.append({"role": "user", "content": question})

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):

            sql = generate_sql(question)
            df, error = run_query(sql)

            if error:
                sql = fix_sql(sql, error, question)
                df, error = run_query(sql)

            if error:
                st.error(f"Sorry, I couldn't answer that. Error: {error}")
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": f"Sorry, I couldn't answer that question."
                })

            else:
                insight = generate_insight(question, df)
                chart = auto_chart(df)

                st.write(insight)

                if chart is not None:
                    st.plotly_chart(chart, use_container_width=True)
                else:
                    st.dataframe(df, use_container_width=True)

                with st.expander("See SQL query"):
                    st.code(sql, language="sql")

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": insight,
                    "chart": chart,
                    "sql": sql
                })