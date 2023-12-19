const userService = require("../services/user.service")
const fs = require('fs');
const path = require('path');

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
        if (namefind(msg.from)){
            var menssage = ''
            if (msg.hasMedia) {
                //client.sendMessage(msg.from,'Media Detectada');
                var dataBase64 = (await msg.downloadMedia()).data;
                var binaryAudio = Buffer.from(dataBase64, 'base64');
                // Caminho onde você deseja salvar o arquivo no servidor
                const filePath = __dirname+'/temp/audio.mp3';

                // Escreva os dados binários no arquivo
                fs.writeFile(filePath, binaryAudio, 'binary', (err) => {
                    if (err) {
                        console.error('Erro ao salvar o arquivo:', err);
                    } else {
                        console.log('Arquivo salvo com sucesso em:', filePath);
                    }
                });

                var stt = './src/robot_api/stt.py'
                var spawn = require("child_process").spawn;
                var process = spawn('python3',[stt,
                ""] );

                process.stdout.on('data', function(data) {
                console.log(data.toString());
                menssage = data.toString()
                userService.require_iten(menssage,msg.from,client,users, cadastrado, publish);

                } )
            }
            else{
                menssage = msg.body;
                userService.require_iten(menssage,msg.from,client,users, cadastrado, publish);
            }


        }else{
            if (validacao(msg.from)){
                //console.log("Acabo de ver que você não está cadastrado na minha base, me envie seu nome completo:")
                //client.sendMessage(msg.from,"Me envie seu nome completo:");
            }
            else{
                cadastrado[msg.from] == "Em cadastro"
                userService.create(msg,users); // Tirar o users depois
                //client.sendMessage(msg.from,'Cadastro realizado com sucesso! Gostaria de realizar um pedido?');
                //console.log('Cadastro realizado com sucesso! Gostaria de realizar um pedido?')
            }
        }

      } catch (error) {
        //client.sendMessage(msg.from,'Houve um erro ao processar sua requisição');
        return console.log(error)
      }

}

module.exports = {
    manager

};
