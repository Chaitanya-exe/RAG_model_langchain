from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import OnlinePDFLoader
from langchain_community.document_loaders import UnstructuredPDFLoader

def prepare(file_path):
    try:
        if file_path:
            loader = UnstructuredPDFLoader(file_path=file_path)
            data = loader.load()
            print("Done loading...")
        else:
            print("upload a pdf file")

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1200, chunk_overlap=300)
        chunks = text_splitter.split_documents(data)
        print("chunks prepared")
        return chunks
    except Exception as e:
        print(f"Error occured: {str(e)}")