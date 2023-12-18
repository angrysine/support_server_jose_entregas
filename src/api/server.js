const { Client, LocalAuth  } = require('whatsapp-web.js');
const qrcode = require('qrcode-terminal');
const dotenv = require('dotenv');
const rclnodejs = require('rclnodejs');
const { QoS } = rclnodejs;



dotenv.config();

const BOT_ID = process.env.BOT_ID;

const client = new Client({
    authStrategy: new LocalAuth(
        {
            clientId:"pedro"
        }
    )
});

const user = require("../api/src/controllers/user.controller")
const dev = require("../api/src/controllers/user.dev")


rclnodejs.init()
const node2 = rclnodejs.createNode('subscription_message_example_node');
node2.createSubscription(
    'std_msgs/msg/String',
    'whatsApp_topic',
    { qos: QoS.profileSystemDefault },
    (msg) => {
        client.sendMessage(BOT_ID,`${msg.data}`)
    }
    );
console.log("Subscribe inicializado")
rclnodejs.spin(node2);
 
const node = rclnodejs.createNode('client');
const publisher = node.createPublisher('std_msgs/msg/String', 'llm_topic');




client.on('qr', (qr) => {
    qrcode.generate(qr,{small:true})
});

client.on('ready', () => {
    console.log('Client is ready!');
});

client.initialize();

client.on('message', async msg => {
    //console.log(msg.from, msg.body)
    //if (msg.fromMe){dev.manager(msg, client);}
    //else{console.log(msg.from)}
    console.log(msg.from)
    if (msg.from == `${BOT_ID}`){user.manager(msg, client, publisher);}
});

