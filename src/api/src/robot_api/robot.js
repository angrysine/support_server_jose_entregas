const net = require("net")

const send = (msg)  => {
    try {
        const client_user = new net.Socket()
        client_user.connect(4000, '127.0.0.1', () =>{
            client_user.write(msg)
        })
        // Evento de recebimento de menssagens do servidor
        client_user.on('data', async (data) => {
            console.log(`Resposta do servidor: ${data.toString()}`);
        });

        // Evento de fechamento da conexão
        client_user.on('end', () => {
            console.log('Conexão fechada pelo servidor.');
        });
    } catch (error) {
        console.log(error)
    }
}


module.exports = {
    send,
};