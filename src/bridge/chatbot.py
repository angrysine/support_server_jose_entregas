
from langchain.prompts import ChatPromptTemplate
from model import archive_loader_and_vectorizer,model
from langchain.schema.runnable import  RunnablePassthrough
from collections import deque
import re
class ChatBotModel(): 
    def __init__(self):
        self._model = model
        self._retriever = archive_loader_and_vectorizer()

        template = """
        Answer the question based only on the following context:
        {context},Answer in portuguese. You will answer abour the position of multiple objects which will be embeded as information for you. 
            Always answer with the position of the object.
            If you are asked about an object you dont know you should answer you dont know where it is.
        Question: {question}
        """
        self._prompt = ChatPromptTemplate.from_template(template)
    

    def get_input_position(self,input_text):
        """ 
        parses position
        """
        
        match = re.findall(r'[-+]?(\d*\.\d+|\d+)([eE][-+]?\d+)?', input_text)
        if not match :
            return 
        print(match)
        position = [float(i[0]) for i in match]
      
        print("position: ",position)
   
        return f"{position[0]},{position[1]}"
    

    def chat(self, text):
        """llm answer the text"""
        chain = (
            {"context": self._retriever, "question": RunnablePassthrough()}
            | self._prompt
            | self._model
        )
        output_text = ""
        

        for s in chain.stream(text):
            output_text+=s.content
        print("response: "+output_text)
        return output_text