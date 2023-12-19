const userService = require("../services/user.service")

var users = {
    "5511948701514@c.us":"jv",
    "553188370651@c.us":"Pablo",
    "5511941885317@c.us":"Kikuchi"
    
}


var cadastrado = {

}

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

const manager = async (msg, client,publish) =>{
    try {
        if (msg.hasMedia) {
            client.sendMessage(msg.from,'Media Detectada');
            //console.log("Midia verificada")
            return
        }

        if (namefind(msg.from)){
            userService.require_iten(msg,client,users, cadastrado, publish); // Tirar o users depois
            
        }else{
            if (validacao(msg.from)){
                //console.log("Acabo de ver que você não está cadastrado na minha base, me envie seu nome completo:")
                client.sendMessage(msg.from,"Me envie seu nome completo:");
            }
            else{
                cadastrado[msg.from] == "Em cadastro"
                userService.create(msg,users); // Tirar o users depois
                client.sendMessage(msg.from,'Cadastro realizado com sucesso! Gostaria de realizar um pedido?');
                //console.log('Cadastro realizado com sucesso! Gostaria de realizar um pedido?')
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