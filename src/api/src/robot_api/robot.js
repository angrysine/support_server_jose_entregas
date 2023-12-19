//const path = require("path")


async function send(msg) {
    try {
        //client.sendMessage(msg.from,'Processando seu pedido');
        console.log('Processando seu pedido')
        publisher.publish(`${msg}`);
        //const spawn = require("child_process").spawn;
        //const pythonProcess = spawn('python3',[path.resolve(__dirname, 'py.py'), msg.body]);


    } catch (error) {
        console.log(error)
    }
}

module.exports = {
    send,
};
