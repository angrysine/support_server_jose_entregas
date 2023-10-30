---
sidebar_position: 2
---

# Arquitetura da Solução

Nossa arquitetura possui 3 partes principais: Aplicação Electron, Backend e Robô de Serviço.

![img alt](/img/arquitetura.png)


## Aplicação Electron

A Aplicação Electron é um software de desktop que permite aos usuários interagirem com um robô por meio de uma interface amigável através de requisições. Neste contexto, os usuários podem se comunicar usando comandos de voz, capturados por um microfone (Speech To Text), ou inserindo texto diretamente no computador do almoxarifado. O sistema também possui a capacidade de converter o texto inserido em fala (Text To Speech), facilitando assim a interação. Além disso, a aplicação se conecta a um servidor backend para listar os itens disponíveis e manter um registro das peças retiradas.

## Backend

O Backend compreende um banco de dados (ainda a ser definido) e uma API implementada em FASTAPI, que oferece rotas de acesso aos itens e ao sistema LLM. O LLM, por sua vez, está conectado ao robô e fornece instruções sobre quais peças devem ser retiradas.

## Robô de Serviço

O Robô de Serviço recebe instruções do Backend por meio de tópicos no ROS (Robot Operating System). Com base nessas instruções, o robô executa rotinas de navegação para recuperar as peças necessárias. Ele mantém um registro para análises posteriores e controle de falhas. Além disso, há uma ideia adicional de disponibilizar um servidor HTTP, permitindo aos usuários interagir diretamente com o robô durante suas operações através de uma aplicação Web.
