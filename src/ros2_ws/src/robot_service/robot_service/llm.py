#! /usr/bin/env python3

from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import  RunnablePassthrough
from langchain.document_loaders import DirectoryLoader, TextLoader
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import chroma

import os
from dotenv import load_dotenv

load_dotenv()
KEY = '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'

class LLM_model():
    def __init__(self) -> None:
        self._model = ChatOpenAI(model="gpt-3.5-turbo", api_key=KEY)
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

    def get_input_position(self,text):
        """
        This function purpose is to get the position from the chatbot
        using a regex, then returning it as a list of float
        """
        input_text = text
        self._logger.info(f'Robot received: {text}')
        match = re.findall(r'[-+]?(\d*\.\d+|\d+)([eE][-+]?\d+)?', input_text)
        position = [float(i[0]) for i in match]
        self._logger.info(f'position: {position}')
        if len(position) > 1:
            return f"{position[0]},{position[1]}"
        self._logger.info(f'Erro ao detectar as peças: { len(position) }')
        return False

    def chat(self, text):

        chain = (
            {"context": self._retriever, "question": RunnablePassthrough()}
            | self._prompt
            | self._model
        )
        return str(chain.invoke(text))
