const rclnodejs = require('rclnodejs');
const path = require("path")

// Create ros object to communicate over your ros connections
rclnodejs.init()
const node = rclnodejs.createNode('client');
const publisher = node.createPublisher('std_msgs/msg/String', 'llm_topic');

//api_topic

function send(msg) {
    try {
        publisher.publish(`${msg}`);
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
