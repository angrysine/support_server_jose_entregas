from django.shortcuts import render
from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = 'home.jinja'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context


class LogsView(TemplateView):
    template_name = 'logs.jinja'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['logs'] = [
            {
                "user": {
                    "name": "ViniciosLugli",
                    "email": "Vinicios.Lugli@sou.inteli.edu.br"
                },
                "item": {
                    "description": "Porca M8",
                    "category": "Parafusos"
                },
                "request": {
                    "quantity": 10,
                    "unit": "unidades",
                },
                "created_at": {
                    "date": "2022-10-18",
                    "time": "20:43:51",
                },
                "status": "Concluído"
            },
            {
                "user": {
                    "name": "AlbertoMiranda",
                    "email": "Alberto.Miranda@sou.inteli.edu.br"
                },
                "item": {
                    "description": "Arruela 8mm",
                    "category": "Parafusos"
                },
                "request": {
                    "quantity": 4,
                    "unit": "unidades",
                },
                "created_at": {
                    "date": "2022-10-18",
                    "time": "14:20:43",
                },
                "status": "Concluído"
            },
            {
                "user": {
                    "name": "CaioMartins",
                    "email": "Caio.Abreu@sou.inteli.edu.br"
                },
                "item": {
                    "description": "Rolamento 608",
                    "category": "Rolamentos"
                },
                "request": {
                    "quantity": 6,
                    "unit": "pares",
                },
                "created_at": {
                    "date": "2022-10-18",
                    "time": "12:00:03",
                },
                "status": "Concluído"
            },
            {
                "user": {
                    "name": "FilipiKikuchi",
                    "email": "Filipi.Kikuchi@sou.inteli.edu.br"
                },
                "item": {
                    "description": "Junta Universal",
                    "category": "Juntas"
                },
                "request": {
                    "quantity": 2,
                    "unit": "conjuntos",
                },
                "created_at": {
                    "date": "2022-10-16",
                    "time": "09:30:00",
                },
                "status": "Sem estoque"
            },
            {
                "user": {
                    "name": "MihaellAlves",
                    "email": "Mihaell.Alves@sou.inteli.edu.br"
                },
                "item": {
                    "description": "Mola 10x50mm",
                    "category": "Molas"
                },
                "request": {
                    "quantity": 18,
                    "unit": "unidades",
                },
                "created_at": {
                    "date": "2022-10-16",
                    "time": "10:03:02",
                },
                "status": "Concluído"
            },
            {
                "user": {
                    "name": "PabloRuan",
                    "email": "Pablo.Viana@sou.inteli.edu.br"
                },
                "item": {
                    "description": "Engrenagem 20 dentes",
                    "category": "Engrenagens"
                },
                "request": {
                    "quantity": 1,
                    "unit": "conjunto",
                },
                "created_at": {
                    "date": "2022-10-14",
                    "time": "07:05:05",
                },
                "status": "Pendente"
            },
            {
                "user": {
                    "name": "JoaoRodrigues",
                    "email": "Joao.Rodrigues@sou.inteli.edu.br"
                },
                "item": {
                    "description": "Engrenagem 24 dentes",
                    "category": "Engrenagens"
                },
                "request": {
                    "quantity": 3,
                    "unit": "conjuntos",
                },
                "created_at": {
                    "date": "2022-10-14",
                    "time": "09:45:25",
                },
                "status": "Concluído"
            }
        ]
        return context
