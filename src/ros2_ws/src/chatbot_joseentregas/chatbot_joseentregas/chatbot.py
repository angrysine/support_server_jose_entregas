#! /usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from langchain.llms import ollama
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import  RunnablePassthrough
from langchain.document_loaders import DirectoryLoader, TextLoader
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import chroma

class ChatBotModel(Node): 
    def __init__(self):
        super().__init__('chatbot_node')
        self._publisher = self.create_publisher(String, 'chatbot_topic', 10)
        self._logger = self.get_logger()
        self._msg = String()
        self._model = ollama.Ollama(model="joseentregas")
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
        loader = DirectoryLoader('../', 
                                glob='**/*.txt',
                                loader_cls=TextLoader,
                                show_progress=True
                            )

        documents = loader.load()

        text_splitter = CharacterTextSplitter(chunk_size=30000, chunk_overlap=0)

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
        output_text = ""
        for s in chain.stream(text):
            output_text+=s
           
            if "<|im_end|>" in output_text:
                break
        output_text = output_text.removesuffix("<|im_end|>")
        self.get_logger().info('Model output: ' + output_text)
        self._msg.data = output_text
        self._publisher.publish(self._msg)
        return output_text

def main():
    rclpy.init()
    chat_model = ChatBotModel()
    while True:
        input_text = input("Enter a command: ")
        if input_text == "exit":
            break
        response = chat_model.chat(input_text)
        chat_model._logger.info('Response: ' + response)
    chat_model.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()
