const require_iten = (msg,client, users, cadastrado, publisher) => {
    
    if (cadastrado[msg.from] == "Em cadastro" || cadastrado[msg.from] == "Pedido finalizado"){
        client.sendMessage(msg.from,`Olá ${users[msg.from]}, em que posso ajudar?`);
        //console.log(`Olá ${users[msg.from]}, em que posso ajudar?`)
        cadastrado[msg.from] = "Em uso"
    }else{
        client.sendMessage(msg.from,'Pedido em processo');
        //console.log('Pedido registrado')
        //console.log(robo.send(msg)) // Criar um loop logico aqui
        publisher.publish(`${msg.body}`);
        //cadastrado[msg.from] = "Pedido finalizado"

    }
}

const create =(msg,users) =>{
    if (users[msg.from] ){
        return
    }else {users[msg.from] = msg.body}
}



// // exportando funções criadas acima
module.exports = {
    require_iten,
    create
};