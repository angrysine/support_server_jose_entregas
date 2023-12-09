const { Client, LocalAuth  } = require('whatsapp-web.js');
const qrcode = require('qrcode-terminal');
const dotenv = require('dotenv');


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

  



