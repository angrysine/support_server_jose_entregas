const robo = require("../robot_api/robot")

//  Item request
const require_iten = (msg,client, users, cadastrado) => {
    console.log(cadastrado)
    if (cadastrado[msg.from] == "Em cadastro" || cadastrado[msg.from] == "Pedido finalizado"){
        client.sendMessage(msg.from,`Olá ${users[msg.from]}, em que posso ajudar?`);
        //console.log(`Olá ${users[msg.from]}, em que posso ajudar?`)
        cadastrado[msg.from] = "Em uso"
    }else{
        client.sendMessage(msg.from,'Pedido em processo');
        robo.send(msg.body,cadastrado[msg.from])

    }
}

//  User registration
const create =(msg,users) =>{
    if (users[msg.from] ){
        return
    }else {users[msg.from] = msg.body}
}



//  Exporting functions created above
module.exports = {
    require_iten,
    create
};
