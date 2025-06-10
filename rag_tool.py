# rag_tool.py
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings, HuggingFacePipeline
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from config import CHROMA_PATH, EMBEDDING_MODEL, LLM_MODEL

def initialize_rag_chain():
    """Initialize the RAG chain for answering queries."""
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    vectorstore = Chroma(persist_directory=CHROMA_PATH, embedding_function=embeddings)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 2})

    # Initialize HuggingFace pipeline for BART
    llm = HuggingFacePipeline.from_model_id(
        model_id=LLM_MODEL,
        task="text2text-generation",
        pipeline_kwargs={
            "max_new_tokens": 200,
            "truncation": True,
            "max_length": 1024,
            "do_sample": True,
            "top_k": 50,
            "top_p": 0.95,
            "temperature": 0.7
        },
        device=-1
    )

    prompt_template = """
    Using the provided context, answer the question in 2-3 clear, concise sentences without repetition. Focus on key details relevant to the question.
    Context: {context}
    Question: {question}
    Answer:
    """
    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])

    rag_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True,
        chain_type_kwargs={"prompt": prompt}
    )
    return rag_chain

def answer_query(rag_chain, query, chat_history):
    """Answer a query using the RAG chain."""
    result = rag_chain.invoke({"query": query})
    answer = result["result"]
    sources = result["source_documents"]
    return answer, sources