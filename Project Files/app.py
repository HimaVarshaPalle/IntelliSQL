import sqlite3
import pandas as pd
import streamlit as st
from google import genai
from datetime import datetime

st.set_page_config(
    page_title="IntelliSQL",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600&family=Syne:wght@400;600;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Syne', sans-serif;
}

/* Background */
.stApp {
    background: #080c14;
    color: #e2e8f0;
}

/* Hide default Streamlit header */
header[data-testid="stHeader"] { background: transparent; }

/* Hero banner */
.hero {
    background: linear-gradient(135deg, #0f172a 0%, #0c1a2e 60%, #0a1628 100%);
    border: 1px solid #1e3a5f;
    border-radius: 16px;
    padding: 32px 36px;
    margin-bottom: 28px;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: '';
    position: absolute;
    top: -40px; right: -40px;
    width: 200px; height: 200px;
    background: radial-gradient(circle, rgba(0,212,255,0.08) 0%, transparent 70%);
    border-radius: 50%;
}
.hero h1 {
    font-size: 2.4rem;
    font-weight: 800;
    background: linear-gradient(90deg, #ffffff 40%, #00d4ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0 0 6px 0;
    font-family: 'Syne', sans-serif;
}
.hero p {
    color: #64748b;
    font-size: 0.95rem;
    margin: 0;
    font-family: 'Syne', sans-serif;
}

/* SQL display box */
.sql-box {
    background: #0d1117;
    border: 1px solid #1e3a5f;
    border-left: 3px solid #00d4ff;
    border-radius: 8px;
    padding: 16px 20px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.88rem;
    color: #7dd3fc;
    white-space: pre-wrap;
    word-break: break-all;
    margin: 12px 0;
}

/* History item */
.hist-item {
    background: #0f172a;
    border: 1px solid #1e293b;
    border-radius: 8px;
    padding: 12px 16px;
    margin-bottom: 8px;
    font-size: 0.85rem;
}
.hist-item .q  { color: #e2e8f0; font-weight: 600; margin-bottom: 4px; }
.hist-item .sql { color: #38bdf8; font-family: 'JetBrains Mono', monospace; font-size: 0.78rem; }
.hist-item .meta { color: #475569; font-size: 0.75rem; margin-top: 4px; }

/* Metric card */
.metric-row {
    display: flex;
    gap: 12px;
    margin: 12px 0;
}
.metric-card {
    background: #0f172a;
    border: 1px solid #1e293b;
    border-radius: 8px;
    padding: 12px 18px;
    flex: 1;
    text-align: center;
}
.metric-card .val { font-size: 1.5rem; font-weight: 800; color: #00d4ff; }
.metric-card .lbl { font-size: 0.75rem; color: #64748b; margin-top: 2px; }

/* Streamlit overrides */
div[data-testid="stTextInput"] input {
    background: #0f172a !important;
    border: 1px solid #1e3a5f !important;
    border-radius: 8px !important;
    color: #e2e8f0 !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 0.95rem !important;
    padding: 12px 16px !important;
}
div[data-testid="stTextInput"] input:focus {
    border-color: #00d4ff !important;
    box-shadow: 0 0 0 2px rgba(0,212,255,0.15) !important;
}
.stButton button {
    background: linear-gradient(135deg, #0ea5e9, #00d4ff) !important;
    color: #080c14 !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 10px 28px !important;
    font-size: 0.9rem !important;
    letter-spacing: 0.5px !important;
}
.stButton button:hover {
    opacity: 0.9 !important;
    transform: translateY(-1px) !important;
}
div[data-testid="stDataFrame"] {
    border: 1px solid #1e293b !important;
    border-radius: 8px !important;
    overflow: hidden !important;
}
section[data-testid="stSidebar"] {
    background: #0a0e1a !important;
    border-right: 1px solid #1e293b !important;
}
</style>
""", unsafe_allow_html=True)

if "history" not in st.session_state:
    st.session_state.history = []
if "question_input" not in st.session_state:
    st.session_state.question_input = ""

with st.sidebar:
    st.markdown("### Configuration")
    api_key = st.text_input(
        "Google API Key",
        type="password",
        placeholder="Paste your API key here",
        help="Get a free key at https://aistudio.google.com/app/apikey"
    )

    st.divider()

    st.markdown("### Table Schema")
    st.code("customers(\n  id,\n  name,\n  city,\n  purchase_amount\n)", language="sql")

    st.divider()

    st.markdown("### Try asking")
    examples = [
        "Show all customers",
        "Who is from Kadapa?",
        "Show highest purchase",
        "Count customers by city",
        "Sort by purchase amount",
    ]
    for ex in examples:
        if st.button(ex, key=f"ex_{ex}", use_container_width=True):
            st.session_state.question_input = ex

    st.divider()

    if st.button(" Clear History", use_container_width=True):
        st.session_state.history = []
        st.success("History cleared!")

    st.caption("IntelliSQL · Powered by Gemini · Built with Streamlit")

st.markdown("""
<div class="hero">
  <h1> IntelliSQL</h1>
  <p>Ask questions about your database in plain English · Gemini converts them to SQL instantly</p>
</div>
""", unsafe_allow_html=True)

col_q, col_btn = st.columns([5, 1])
with col_q:
    question = st.text_input(
        "question",
        value=st.session_state.question_input,
        placeholder="e.g.  Show all customers from Hyderabad",
        label_visibility="collapsed",
    )
with col_btn:
    run = st.button("⚡ Run", use_container_width=True)

def generate_sql(question: str, key: str) -> str:
    client = genai.Client(api_key=key)
    prompt = f"""
    You are an expert SQL assistant.

    Table:
    customers(id, name, city, purchase_amount)

    Convert the question below to a valid SQLite SQL query.
    Return ONLY the SQL query — no explanation, no markdown, no backticks.

    Question: {question}
    """
    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=prompt
    )
    sql = response.text.strip()
    if sql.startswith("```"):
        lines = sql.splitlines()
        sql = "\n".join(lines[1:-1]).strip()
    return sql

def run_query(sql: str):
    conn   = sqlite3.connect("sales.db")
    cursor = conn.cursor()
    cursor.execute(sql)
    columns = [d[0] for d in cursor.description] if cursor.description else []
    rows    = cursor.fetchall()
    conn.close()
    return columns, rows

if run and question.strip():

    if not api_key:
        st.warning("Please enter your Google API Key in the sidebar.", icon="🔑")
        st.stop()

    with st.spinner(" Gemini is thinking..."):
        try:
            sql_query = generate_sql(question, api_key)
        except Exception as e:
            st.error(f"Gemini error: {e}")
            st.stop()

    st.markdown("**Generated SQL:**")
    st.markdown(f'<div class="sql-box">{sql_query}</div>', unsafe_allow_html=True)

    try:
        columns, rows = run_query(sql_query)

        if not rows:
            st.info("Query ran successfully but returned no rows.")
        else:
            df = pd.DataFrame(rows, columns=columns)

            st.markdown(f"""
            <div class="metric-row">
                <div class="metric-card"><div class="val">{len(rows)}</div><div class="lbl">Rows</div></div>
                <div class="metric-card"><div class="val">{len(columns)}</div><div class="lbl">Columns</div></div>
            </div>
            """, unsafe_allow_html=True)

            st.dataframe(df, use_container_width=True)

        st.session_state.history.insert(0, {
            "question": question,
            "sql":      sql_query,
            "rows":     len(rows) if rows else 0,
            "time":     datetime.now().strftime("%H:%M:%S"),
        })
        st.session_state.question_input = ""

    except Exception as e:
        st.error(f"Query error: {e}")

if st.session_state.history:
    st.divider()
    st.markdown("### Query History")
    for entry in st.session_state.history:
        st.markdown(f"""
        <div class="hist-item">
            <div class="q"> {entry['question']}</div>
            <div class="sql">{entry['sql']}</div>
            <div class="meta"> {entry['time']} &nbsp;·&nbsp; {entry['rows']} rows returned</div>
        </div>
        """, unsafe_allow_html=True)

elif not run:
    st.markdown("""
    <div style="text-align:center; padding:60px 0; color:#334155;">
        <div style="font-size:3rem;"></div>
        <div style="font-size:1.1rem; font-weight:700; color:#475569; margin-top:12px;">
            Ask anything about your database
        </div>
        <div style="font-size:0.88rem; margin-top:8px; color:#334155;">
            Type a question above or pick an example from the sidebar
        </div>
    </div>
    """, unsafe_allow_html=True)
