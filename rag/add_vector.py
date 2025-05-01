from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain_ollama import ChatOllama
from .chains import userChains
import ollama

ollama.pull("nomic-embed-text")

def prepare_chain(chunks):
    try:
        vector_db = Chroma.from_documents(
        documents=chunks,
        embedding=OllamaEmbeddings(model="nomic-embed-text"),
        collection_name="simple-rag"
        )

        model = "llama3.2"
        llm = ChatOllama(model=model)

        QUERY_PROMPT = PromptTemplate(
            input_variables=["question"],
            template="""
        You are an AI language model assistant. Your task is to generate
        five different versions of the given user questions to retrieve relevant
        documents from a vector database. By generating multiple perspectives of the user 
        questions, your goal is to help the user overcome some of the limitations of the 
        distance-based similarity search. Provide these alternative questions separated
        by newlines
        Original questions: {question}
        """
        )

        retreiver = MultiQueryRetriever.from_llm(vector_db.as_retriever(), llm=llm, prompt=QUERY_PROMPT)
        template = """
        Answer the question based only on the following context
        {context}
        Question: {question}
        """

        prompt = ChatPromptTemplate.from_template(template)

        chain = (
            {"context":retreiver, "question":RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
        )

        userChains.append(chain)
        print("vector prepared")
    except Exception as e:
        print(f"Error occured {str(e)}")