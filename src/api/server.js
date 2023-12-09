const path = require("path")
require("http://static.robotwebtools.org/roslibjs/current/roslib.min.js")

// Create ros object to communicate over your Rosbridge connection
const client_user = new ROSLIB.Ros({ url: "ws://127.0.0.1:9090" });


ros.on("connection", () => {
    console.log("Conexão com ROS estabelecida.")
  });

client_user.on('data', (data) => {
    console.log(`Resposta do servidor: ${data.toString()}`);
    // Fecha a conexão após receber a resposta
});

// Evento de fechamento da conexão
client_user.on('end', () => {
    console.log('Conexão fechada pelo servidor.');
});



// Criar um publicador para o tópico /my_publish_topic
const my_publish_topic_publisher = new ROSLIB.Topic({
    ros,
    name: '/my_publish_topic',
    messageType: 'std_msgs/String'
});

// Função para publicar uma mensagem no tópico
function publishMessage(messageText) {
    const message = new ROSLIB.Message({
        data: messageText
    });

    // Publicar a mensagem no tópico
    my_publish_topic_publisher.publish(message);
}




function send(msg) {
    try {
        client_user.write(msg)
        publishMessage(msg);
        const spawn = require("child_process").spawn;
        const pythonProcess = spawn('python3',[path.resolve(__dirname, 'tts.py'), msg]);
        return "Mensagem após cliente send";
 
    } catch (error) {
        console.log(error)
    }
}


module.exports = {
    send,
};


