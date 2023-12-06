const { Client, LocalAuth  } = require('whatsapp-web.js');
const qrcode = require('qrcode-terminal');
const client = new Client({
    authStrategy: new LocalAuth(
        {
            clientId:"pedro"
        }
    )
});
const user = require("../api/src/controllers/user.controller")



client.on('qr', (qr) => {
    qrcode.generate(qr,{small:true})
});

client.on('ready', () => {
    console.log('Client is ready!');
});

client.initialize();

client.on('message_create', async msg => {
    user.manager(msg, client)
    // if(msg.hasMedia) {
    //     const media = await msg.downloadMedia();
        
    // }
    // else{
    //     user.require_iten(msg.body,client)
    // }

});

  



