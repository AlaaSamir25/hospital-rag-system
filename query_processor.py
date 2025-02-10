from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
from vector_store import get_vector_store
from database import fetch_all_records, tables
import os

vector_store = get_vector_store()
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key="gemini-api-key",
    temperature=0
)

def is_generic_query(query: str) -> bool:
    query_lower = query.strip().lower()
    return query_lower in {"hi", "hello", "hey"} or any(
        phrase in query_lower 
        for phrase in ["how can you help", "what can you do", "tell me about", "help me"]
    )

def is_out_of_context(query: str) -> bool:
    query_lower = query.strip().lower()
    keywords = ["physician", "doctor", "schedule", "price", "specialty", "hospital"]
    return not any(kw in query_lower for kw in keywords)

def process_query(query: str) -> str:
    if is_generic_query(query):
        return ("Welcome to Pain & Go Hospital! I can help with doctor schedules, "
                "service pricing, and hospital policies. How can I assist you?")
    
    if is_out_of_context(query):
        policy_records = fetch_all_records("Policy", tables["Policy"])
        policy_context = "\n".join([f"{k}: {v}" for record in policy_records for k, v in record.items()])
        prompt = PromptTemplate(
            template="The user asked: {query}\n\nHere's our policy info:\n{context}",
            input_variables=["query", "context"]
        )
        chain = prompt | llm | StrOutputParser()
        return chain.invoke({"query": query, "context": policy_context})
    
    docs = vector_store.similarity_search(query, k=5)
    context = "\n\n".join([doc.page_content for doc in docs])
    prompt = PromptTemplate(
        template="Answer warmly using this context:\n{context}\n\nQuestion: {query}\nFriendly Answer:",
        input_variables=["query", "context"]
    )
    chain = prompt | llm | StrOutputParser()
    return chain.invoke({"query": query, "context": context})