# Whatsapp

## Fluxo Atual

Abaixo, o fluxo do usuário pelo WhatsApp em um diagrama de blocos:

<iframe width="800" height="450" src="https://whimsical.com/embed/Ay2sLu2xp9JkxeNW7okHEx"></iframe>

## Aquivos e Funções Utilizadas

Abaixo os principais arquivos e funções utilizadas na interface whatsapp robô.

### API - server.js
<p><b>Caminho do diretório:</b> grupo1/src/api/server.js</p>

```javascript
// Imports
const { Client, LocalAuth  } = require('whatsapp-web.js');
const qrcode = require('qrcode-terminal');
const dotenv = require('dotenv');

const user = require("../api/src/controllers/user.controller")
const dev = require("../api/src/controllers/user.dev")


//  Environment settings
dotenv.config();
const BOT_ID = process.env.BOT_ID;
const client = new Client({
    authStrategy: new LocalAuth(
        {
            clientId:"pedro"
        }
    )
});
```

```javascript
// Usage of the WhatsApp client
client.on('qr', (qr) => {
    qrcode.generate(qr,{small:true})
});

client.on('ready', () => {
    console.log('Client is ready!');
});

client.initialize();

client.on('message_create', async msg => {
    if (msg.fromMe){dev.manager(msg, client);}
    if (msg.to == `${BOT_ID}`){user.manager(msg, client);}
});
```

### API - user.controller.js
<p><b>Caminho do diretório:</b> grupo1/src/api/controllers/user.controller.js</p>

```javascript
// Session management
var users = {

}


var cadastrado = {

}
```

```javascript
//  Validations
const namefind = (numero) => {
    if (users[numero]){
        console.log("User cadastrado ----> ", users[numero])
        return true
    }
    return  false

}

const validacao = (numero) => {
    if (cadastrado[numero]){
        console.log("User cadastrado")
        return false
    }
    else{
        cadastrado[numero] = "Em cadastro"
        return true
    }

}
```


### API - user.service.js
<p><b>Caminho do diretório:</b> grupo1/src/api/services/user.service.js</p>

```javascript
//  Item request
const require_iten = (msg,client, users, cadastrado) => {
    console.log(cadastrado)
    if (cadastrado[msg.from] == "Em cadastro" || cadastrado[msg.from] == "Pedido finalizado"){
        client.sendMessage(msg.from,`Olá ${users[msg.from]}, em que posso ajudar?`);
        //console.log(`Olá ${users[msg.from]}, em que posso ajudar?`)
        cadastrado[msg.from] = "Em uso"
    }else{
        client.sendMessage(msg.from,'Pedido em processo');
        robo.send(msg.body,cadastrado[msg.from])

    }
}
```

```javascript
//  User registration
const create =(msg,users) =>{
    if (users[msg.from] ){
        return
    }else {users[msg.from] = msg.body}
}
```

### Robot Service - llm_robot.py
<p><b>Caminho do diretório:</b> grupo1\src\ros2_ws\src\robot_service\robot_service\llm_robot.py</p>


```python
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
```


```python
    def listener_callback(self, msg):
        """
        This function purpose is to processes data from the llm_topic
        """
        self._logger.info(f'Robot received: {msg.data}')
        self._logger.warning('Passing data to navigation controller')
        self.chat(msg.data)
```


```python
    def chat(self, text):
        output_text = self._model.chat(text)
        self.get_logger().info('Model output: ' + output_text)
        self._msg.data = self.get_input_position(output_text)
        self._publisher.publish(self._msg)
```


```python
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
```

### Robot Service - llm.py
<p><b>Caminho do diretório:</b> grupo1\src\ros2_ws\src\robot_service\robot_service\llm.py</p>


```python
class LLM_model():
    def __init__(self) -> None:
        self._model = ollama.Ollama(model="dolphin2.2-mistral")
        self._retriever = self.archive_loader_and_vectorizer()
        template = """Answer the question based only on the following context:
        {context}
        Question: {question}
        """
        self._prompt = ChatPromptTemplate.from_template(template)
```

```python
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
```

```python
    def chat(self, text):

        chain = (
            {"context": self._retriever, "question": RunnablePassthrough()}
            | self._prompt
            | self._model
        )
        return str(chain.invoke(text))
```

### Robot Service - robot.py
<p><b>Caminho do diretório:</b> grupo1\src\ros2_ws\src\robot_service\robot_service\llm.py</p>


```python
class Robot(Node):
    def __init__(self):
        super().__init__('robot_node')
        self._publisher = self.create_publisher(String, 'whatsApp_topic', 10)
        self._subscriber = self.create_subscription(
            String,
            'chatbot_topic',
            self.listener_callback,
            10)
        self._logger = self.get_logger()
        self._msg = String()
        self._nav = Navigation()

```

```python
    def listener_callback(self, msg):
        """
        This function purpose is to receive the data from the chatbot topic
        """
        self._logger.info(f'Robot received: {msg.data}')
        self._logger.warning('Passing data to navigation controller')
        self._msg = msg.data
        return self._msg

```

```python
    def get_input_position(self):
        """
        This function purpose is to get the position from the chatbot
        using a regex, then returning it as a list of integers
        """
        input_text = self.listener_callback()
        match = re.findall(r'\b\d+\b', input_text)
        position = [float(match) for i in match[-2:]]
        return position

```

```python
    def move_towards_required_position(self):
        """
        This function purpose is to create a pose and move the robot
        """
        position = self.get_input_position()
        self._nav.create_pose(position[0], position[1], 0.0)

```
```python
    def cheking_status(self):
        """
        Checks the status of a task after moving towards the required position.
        Returns:
        bool: True if the task is completed successfully, False otherwise.
        """
        self.move_towards_required_position()
        task_status = self._nav.robot_navigation_status()

        return task_status if task_status == TaskResult.SUCCEEDED else False

```
