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
import re


class ChatBotModel(Node):
    def __init__(self):
        super().__init__('llm_node')
        self._publisher = self.create_publisher(String, 'chatbot_topic', 10)
        self._subscriber = self.create_subscription(
            String,
            'llm_topic',
            self.listener_callback,
            10)
        self._logger = self.get_logger()
        self._msg = String()

        self._model = ollama.Ollama(model="dolphin2.2-mistral")
        self._retriever = self.archive_loader_and_vectorizer()
        template = """Answer the question based only on the following context:
        {context}

        Question: {question}
        """
        self._prompt = ChatPromptTemplate.from_template(template)

    def listener_callback(self, msg):
        """
        This function purpose is to processes data from the llm_topic
        """
        self._logger.info(f'Robot received: {msg.data}')
        self._logger.warning('Passing data to navigation controller')
        self.chat(msg.data)
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

    def chat(self, text):

        chain = (
            {"context": self._retriever, "question": RunnablePassthrough()}
            | self._prompt
            | self._model
        )
        output_text = str(chain.invoke(text))
        self.get_logger().info('Model output: ' + output_text)
        self._msg.data = self.get_input_position(output_text)
        self._publisher.publish(self._msg)
        return output_text

def main():
    rclpy.init()
    node = ChatBotModel()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()
