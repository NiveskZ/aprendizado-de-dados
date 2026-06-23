import os
from typing import TypedDict, Annotated, Sequence, Literal
from dotenv import load_dotenv

from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.tools import create_retriever_tool
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import MemorySaver
from langchain_community.utilities import SQLDatabase
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite",
    api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0,
    disable_streaming=True
)

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)
vectorstore = Chroma(
    persist_directory="./chroma_db",
    embedding_function=embeddings,
    collection_name="hr_manual"
)
retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

rag_tool = create_retriever_tool(
    retriever,
    name="busca_manual_rh",
    description="Use para buscar políticas de RH, férias, benefícios, banco de horas e regras da ChocolaTech."
)

mysql_url = os.getenv("MYSQL_URL")  # mysql+pymysql://usuario:senha@host:porta/banco
db = SQLDatabase.from_uri(mysql_url)
sql_tool = QuerySQLDataBaseTool(db=db)
sql_tool.description = (
    "Use para buscar saldo de férias e banco de horas de um funcionário. "
    "Input: query SQL para a tabela funcionarios usando LIKE com %nome% "
    "(ex.: SELECT nome, saldo_ferias, banco_horas FROM funcionarios WHERE nome LIKE '%joão silva%'). "
    "Colunas disponíveis: nome, email, departamento, cargo, saldo_ferias, banco_horas, regime."
)

tools = [rag_tool, sql_tool]

SYSTEM_PROMPT = """Você é o HR Buddy, assistente virtual de RH da ChocolaTech.
REGRAS:
1. Sempre responda em português.
2. Responda APENAS dúvidas relacionadas a RH."""

class EstadoAgente(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]

llm_com_tools = llm.bind_tools(tools)

def agente(estado: EstadoAgente) -> EstadoAgente:
    mensagens = [SystemMessage(content=SYSTEM_PROMPT)] + list(estado["messages"])
    resposta = llm_com_tools.invoke(mensagens)
    return {**estado, "messages": [resposta]}

def deve_continuar(estado: EstadoAgente) -> Literal["tools", "__end__"]:
    ultima = estado["messages"][-1]
    if hasattr(ultima, "tool_calls") and ultima.tool_calls:
        return "tools"
    return "__end__"

executor_tools = ToolNode(tools)

builder = StateGraph(EstadoAgente)
builder.add_node("agente", agente)
builder.add_node("tools", executor_tools)
builder.set_entry_point("agente")
builder.add_conditional_edges("agente", deve_continuar)
builder.add_edge("tools", "agente")

memoria = MemorySaver()
hr_app = builder.compile(checkpointer=memoria)

def conversar(mensagem: str, session_id: str) -> str:
    resultado = hr_app.invoke(
        {"messages": [HumanMessage(content=mensagem)]},
        config={"configurable": {"thread_id": session_id}}
    )
    return resultado["messages"][-1].content

if __name__ == "__main__":
    print(conversar("Oi", "teste-1"))
    print(conversar("Como funciona a política de trabalho remoto?", "teste-1"))
    print(conversar("Quantos dias de férias tenho direito?", "teste-1"))
    print(conversar("Quem foi campeão do mundo de 1950?", "teste-1"))