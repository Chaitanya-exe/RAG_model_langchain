from langchain_community.document_loaders import UnstructuredPDFLoader
from langchain_community.document_loaders import OnlinePDFLoader
from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain.retrievers.multi_query import MultiQueryRetriever
import ollama

model = "llama3.2"
doc = "./data/CD_051.pdf"


    

if doc:
    loader = UnstructuredPDFLoader(file_path=doc)
    data = loader.load()
    print("Done loading...")
else:
    print("upload a pdf file")

content = data[0].page_content

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1200, chunk_overlap=300)
chunks = text_splitter.split_documents(data)
print("Done splitting...")

ollama.pull("nomic-embed-text")

vector_db = Chroma.from_documents(
    documents=chunks,
    embedding=OllamaEmbeddings(model="nomic-embed-text"),
    collection_name="simple-rag"
)

print("Done adding vector to database...")

# model preparation

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

while True:
    user_question = str(input("Enter the question about the file: "))
    res = chain.invoke(input=(user_question,))
    print(res)