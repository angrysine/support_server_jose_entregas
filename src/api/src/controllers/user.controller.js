const userService = require("../services/user.service")


// Session management
var users = {

}


var cadastrado = {

}

//  Validations
const namefind = (numero) => {
    if (users[numero]){
        console.log("User cadastrado ----> ", users[numero])
        return true
    }
    return  false

}

const validacao = (numero) => {
    if (cadastrado[numero]){
        console.log("User cadastrado")
        return false
    }
    else{
        cadastrado[numero] = "Em cadastro"
        return true
    }

}


// Chat manager
const manager = async (msg, client) =>{
    try {
        if (msg.hasMedia) {
            client.sendMessage(msg.from,'Media Detectada');
            return
        }

        if (namefind(msg.from)){
            userService.require_iten(msg,client,users, cadastrado);

        }else{
            if (validacao(msg.from)){

                client.sendMessage(msg.from,"Me envie seu nome completo:");
            }
            else{
                cadastrado[msg.from] == "Em cadastro"
                userService.create(msg,users);
                client.sendMessage(msg.from,'Cadastro realizado com sucesso! Gostaria de realizar um pedido?');

            }
        }

      } catch (error) {
        client.sendMessage(msg.from,'Houve um erro ao processar sua requisição');
        return console.log(error)
      }

}

module.exports = {
    manager

};
