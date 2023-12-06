const robo = require("../robot_api/robot")

const require_iten = (msg,client, users, cadastrado) => {
    console.log(cadastrado)
    if (cadastrado[msg.from] == "Em cadastro" || cadastrado[msg.from] == "Pedido finalizado"){
        //client.sendMessage(msg.from,`Olá ${users[msg.from]}, em que posso ajudar?`);
        console.log(`Olá ${users[msg.from]}, em que posso ajudar?`)
        cadastrado[msg.from] = "Em uso"
    }else{
        //client.sendMessage(msg.from,'Pedido registrado');
        console.log('Pedido registrado')
        robo.sand(msg.body) // Criar um loop logico aqui
        cadastrado[msg.from] = "Pedido finalizado"

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