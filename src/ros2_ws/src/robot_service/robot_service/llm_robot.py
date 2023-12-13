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
from robot_service.llm import LLM_model
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
        self._model = LLM_model()
    def listener_callback(self, msg):
        """
        This function purpose is to processes data from the llm_topic
        """
        self._logger.info(f'Robot received: {msg.data}')
        self._logger.warning('Passing data to navigation controller')
        self.chat(msg.data)
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
        return str(position)

    def chat(self, text):
        output_text = self._model.chat(text)
        self.get_logger().info('Model output: ' + output_text)
        self._msg.data = self.get_input_position(output_text)
        self._publisher.publish(self._msg)

def main():
    rclpy.init()
    node = ChatBotModel()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
if __name__ == "__main__":
    main()
