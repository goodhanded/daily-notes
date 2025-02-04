from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from application.search import SearchEngineProtocol
from domain.search import SearchResult
from infrastructure.langchain import LangchainDocumentMapper as mapper

class FAISSSearchEngine(SearchEngineProtocol):
    def __init__(self, index_path: str, num_results: int = 5):
        self.index_path = index_path
        self.num_results = num_results

    def search(self, query) -> SearchResult:

        # Define embeddings (OpenAI in this example)
        embeddings = OpenAIEmbeddings()

        # Load FAISS index
        vector_store = FAISS.load_local(self.index_path, embeddings=embeddings, allow_dangerous_deserialization=True)

        # Search
        print(f'Searching for: {query}')
        print(f'Index path: {self.index_path}')
        print(f'K = {self.num_results}')
        langchain_docs = vector_store.similarity_search(query, k=self.num_results)
        print(f'{len(langchain_docs)} documents found before mapping')
        docs = mapper.from_langchain(langchain_docs)
        print(f'{len(docs)} documents found after mapping')

        return SearchResult(
            query=query,
            success=True,
            message="Search complete",
            results=docs)
