---
sidebar_position: 1
---

# Requisitos Funcionais & Não Funcionais

<div style={{display: "flex"}}>

<div style={{width:"50%"}}>

| N°  | Requisito | Descrição                                                                              |
| --- | --------- | -------------------------------------------------------------------------------------- |
| 1   | Funcional | Capacidade do sistema entender a peça que deve ser pega por fala ou texto              |
| 2   | Funcional | Capacidade de mapear espaços que o robô percorreu                                      |
| 3   | Funcional | Robô deve ser capaz de percorrer o caminho até um item específico em um espaço mapeado |
| 4   | Funcional | Deve haver controle automático do inventário das peças retiradas pelo robô             |
| 5   | Funcional | Deve haver uma aplicação que permita ver o inventário                                  |
| 6   | Funcional | Deve haver uma aplicação que permita ativar o robô para pegar um item                  |
| 7   | Funcional | A aplicação deve ter um método de parar o robô                                         |

</div>

<div style={{width:"50%", paddingLeft:"50px"}}>

| Nº  | Tipo          | Descrição                                                                                                                     |
| --- | ------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| 1   | Não-funcional | O sistema deve ser capaz de processar comandos de fala ou texto em menos de 2 segundos                                        |
| 2   | Não-funcional | O sistema deve ser capaz de mapear um espaço de 1000 metros quadrados em não mais que 15 minutos                              |
| 3   | Não-funcional | O sistema de controle de inventário deve ser capaz de atualizar o status de um item em menos de 1 segundo após o robô pegá-lo |
| 4   | Não-funcional | A aplicação deve ser capaz de exibir os itens disponíveis em menos de 3 segundos após a solicitação                           |
| 5   | Não-funcional | A aplicação deve ser capaz de ativar o robô para pegar um item em menos de 5 segundos após a solicitação                      |
| 6   | Não-funcional | A aplicação deve ser capaz de exibir o inventário atualizado em menos de 10 segundos após a solicitação                       |
| 7   | Não-funcional | A aplicação deve ser capaz de parar o robô em menos de 10 segundo após a solicitação                                          |
| 8   | Não-funcional | O sistema deve ser capaz de operar por pelo menos 8 horas contínuas sem falhas                                                |
| 9   | Não-funcional | O sistema deve garantir a segurança dos dados do inventário, permitindo apenas acesso autorizado                              |
| 10  | Não-funcional | O Robô deve ser capaz de servir as páginas, em menos de 2 segundos, relacionadas ao controle do robô.                         |

</div>
</div>
