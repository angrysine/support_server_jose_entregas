const net = require("net")

const client_user = new net.Socket()
client_user.connect(4000, '127.0.0.1', () =>{
    console.log("conetado com o robô")
})

client_user.on('data', (data) => {
    console.log(`Resposta do servidor: ${data.toString()}`);
    // Fecha a conexão após receber a resposta
});

// Evento de fechamento da conexão
client_user.on('end', () => {
    console.log('Conexão fechada pelo servidor.');
});

function send(msg) {
    try {
        client_user.write(msg)
        return "Menssagem após cliente sand"
 
    } catch (error) {
        console.log(error)
    }
}


module.exports = {
    send,
};