from langchain.llms import ollama
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import  RunnablePassthrough
from langchain.document_loaders import DirectoryLoader, TextLoader
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import chroma

class LLM_model():
    def __init__(self) -> None:
        self._model = ollama.Ollama(model="dolphin2.2-mistral")
        self._retriever = self.archive_loader_and_vectorizer()
        template = """Answer the question based only on the following context:
        {context}
        Question: {question}
        """
        self._prompt = ChatPromptTemplate.from_template(template)

    def archive_loader_and_vectorizer(self):
        """
        This function loads txt documents from current directory
        and vectorizes them
        """
        loader = DirectoryLoader('./',
                                glob='**/items.txt',
                                loader_cls=TextLoader,
                                show_progress=True
                            )
        documents = loader.load()
        text_splitter = CharacterTextSplitter(chunk_size=300, chunk_overlap=0)
        docs = text_splitter.split_documents(documents)
        embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
        vectorstore = chroma.Chroma.from_documents(docs, embedding_function)
        retriever = vectorstore.as_retriever()
        return retriever

    def chat(self, text):

        chain = (
            {"context": self._retriever, "question": RunnablePassthrough()}
            | self._prompt
            | self._model
        )
        return str(chain.invoke(text))
