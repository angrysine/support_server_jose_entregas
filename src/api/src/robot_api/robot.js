const path = require("path")
const rclnodejs = require('rclnodejs');
const { QoS } = rclnodejs;



// Create ros object to communicate over your ros connections
rclnodejs.init().then(() => {
    const node = rclnodejs.createNode('subscription_message_example_node');

    node.createSubscription(
        'std_msgs/msg/String',
        'whatsApp_topic',
        { qos: QoS.profileSystemDefault },
        (msg) => {
          console.log(`Received message: ${typeof msg}`, msg);
        }
      );
    console.log("Subscribe inicializado")
    rclnodejs.spin(node);
  })
  .catch((e) => {
    console.log(e);
  });
const node = rclnodejs.createNode('client');
const publisher = node.createPublisher('std_msgs/msg/String', 'llm_topic');


async function send(msg) {
    try {
        //client.sendMessage(msg.from,'Processando seu pedido');
        console.log('Processando seu pedido')
        publisher.publish(`${msg}`);
        const spawn = require("child_process").spawn;
        //const pythonProcess = spawn('python3',[path.resolve(__dirname, 'py.py'), msg.body]);


    } catch (error) {
        console.log(error)
    }
}

module.exports = {
    send,
};
