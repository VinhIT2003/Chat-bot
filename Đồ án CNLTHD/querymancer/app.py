import random

import streamlit as st
from dotenv import load_dotenv
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

from querymancer.agent import ask, create_history
from querymancer.config import Config
from querymancer.models import create_llm
from querymancer.tools import get_available_tools, with_sql_cursor
import pyodbc

load_dotenv()

LOADING_MESSAGES = [
    "Consulting the ancient tomes of SQL wisdom...",
    "Casting query spells on your database...",
    "Summoning data from the digital realms...",
    "Deciphering your request into database runes...",
    "Brewing a potion of perfect query syntax...",
    "Channeling the power of database magic...",
    "Translating your words into the language of tables...",
    "Waving my SQL wand to fetch your results...",
    "Performing database divination...",
    "Aligning the database stars for optimal results...",
    "Consulting with the database spirits...",
    "Transforming natural language into database incantations...",
    "Peering into the crystal ball of your database...",
    "Opening a portal to your data dimension...",
    "Enchanting your request with SQL magic...",
    "Invoking the ancient art of query optimization...",
    "Reading between the tables to find your answer...",
    "Conjuring insights from your database depths...",
    "Weaving a tapestry of joins and filters...",
    "Preparing a feast of data for your consideration...",
]

@st.cache_resource(show_spinner=False)
def get_model() -> BaseChatModel:
    llm = create_llm(Config.MODEL)
    llm = llm.bind_tools(get_available_tools())
    return llm

def load_css(css_file):
    with open("C:/Users/yonor/OneDrive/Documents/Đồ án CNLTHD/querymancer/assets/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.set_page_config(
    page_title="Querymancer",
    page_icon="🪄",
    layout="centered",
    initial_sidebar_state="collapsed",
)

def get_db_size():
    conn = Config.connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            SUM(size * 8 / 1024) AS db_size_mb
        FROM 
            sys.master_files
        WHERE 
            database_id = DB_ID('test')
    """)
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else 0

load_css("assets/style.css")

st.header("Querymancer")
st.subheader("Talk to your database using natural language")

with st.sidebar:
    st.write("# Database Information")
    st.write("**Kết nối CSDL:** Đang sử dụng SQL Server với máy chủ 'YONORIKOMANA\\QUOCDUONG'")

    db_size = get_db_size() 
    st.write(f"**Size:** {db_size:.2f} MB")

    with with_sql_cursor() as cursor:
        cursor.execute(
            """
            SELECT name FROM sys.tables
            WHERE name NOT LIKE 'sys%' AND name NOT LIKE 'queue%';
            """
        )
        tables = [row[0] for row in cursor.fetchall()]
        st.write("**Tables:**")
        for table in tables:
            cursor.execute(f"SELECT count(*) FROM {table};")
            count = cursor.fetchone()[0]
            st.write(f"- `{table}` ({count} rows)")


if "messages" not in st.session_state:
    st.session_state.messages = create_history()

for message in st.session_state.messages:
    if type(message) is SystemMessage:
        continue
    is_user = type(message) is HumanMessage
    avatar = "🧑‍💻" if is_user else "🤖"
    with st.chat_message("user" if is_user else "ai", avatar=avatar):
        st.markdown(message.content)

if prompt := st.chat_input("Type your message..."):
    with st.chat_message("user", avatar="🧑‍💻"):
        st.session_state.messages.append(HumanMessage(prompt))
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="🤖"):
        message_placeholder = st.empty()
        message_placeholder.status(random.choice(LOADING_MESSAGES), state="running")
        response = ask(prompt, st.session_state.messages, get_model())
        message_placeholder.markdown(response)
        st.session_state.messages.append(AIMessage(response))