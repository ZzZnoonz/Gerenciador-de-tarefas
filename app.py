from flask import Flask, render_template, request, jsonify, make_response
from datetime import datetime, date
import io
import csv

from services.gerenciador import Gerenciador
from models.tarefa import TarefaSimples

app = Flask(__name__)
gerenciador = Gerenciador()

def popular_dados_iniciais():
    if not gerenciador._tarefas:
        t1 = TarefaSimples(
            "Aprender Flask", 
            "Criar rotas de API para o projeto de POO.", 
            date(2025, 8, 1), 
            "14:00"
        )
        t1.toggle_status() # Marcar como concluído para exemplo
        
        t2 = TarefaSimples(
            "Ir ao supermercado", 
            "Comprar itens para a semana, não esquecer o café.", 
            date.today(), 
            "18:30"
        )
        gerenciador.adicionar_tarefa(t1)
        gerenciador.adicionar_tarefa(t2)
        print(">>> Dados iniciais foram carregados!")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/tarefas", methods=['GET'])
def get_tarefas():
    lista_de_tarefas_em_dict = [t.to_dict() for t in gerenciador._tarefas if hasattr(t, 'id')]
    return jsonify(lista_de_tarefas_em_dict)

@app.route("/api/tarefas", methods=['POST'])
def add_tarefa():
    dados = request.get_json()
    campos_obrigatorios = ['titulo', 'descricao', 'data_entrega', 'horario']
    if not all(campo in dados and dados[campo] for campo in campos_obrigatorios):
        return jsonify({"erro": "Todos os campos são obrigatórios"}), 400

    try:
        data_obj = datetime.strptime(dados['data_entrega'], '%Y-%m-%d').date()
    except ValueError:
        return jsonify({"erro": "Formato de data inválido."}), 400

    nova_tarefa = TarefaSimples(
        titulo=dados['titulo'],
        descricao=dados['descricao'],
        data_entrega=data_obj,
        horario=dados['horario']
    )
    gerenciador.adicionar_tarefa(nova_tarefa)
    return jsonify(nova_tarefa.to_dict()), 201

@app.route("/api/tarefas/<int:tarefa_id>", methods=['PUT', 'DELETE'])
def update_or_delete_tarefa(tarefa_id):
    tarefa = next((t for t in gerenciador._tarefas if hasattr(t, 'id') and t.id == tarefa_id), None)
    if not tarefa:
        return jsonify({"erro": "Tarefa não encontrada"}), 404

    if request.method == 'DELETE':
        gerenciador._tarefas.remove(tarefa)
        return jsonify({"mensagem": "Tarefa deletada com sucesso"}), 200

    if request.method == 'PUT':
        dados = request.get_json()
        tarefa._titulo = dados.get('titulo', tarefa.titulo)
        tarefa._descricao = dados.get('descricao', tarefa.descricao) # Atualiza o atributo protegido
        tarefa._horario = dados.get('horario', tarefa._horario)
        if 'data_entrega' in dados and dados['data_entrega']:
            tarefa._data_entrega = datetime.strptime(dados['data_entrega'], '%Y-%m-%d').date()
        return jsonify(tarefa.to_dict()), 200

# NOVA ROTA: Alternar o status da tarefa
@app.route("/api/tarefas/<int:tarefa_id>/toggle-status", methods=['POST'])
def toggle_task_status(tarefa_id):
    tarefa = next((t for t in gerenciador._tarefas if hasattr(t, 'id') and t.id == tarefa_id), None)
    if not tarefa:
        return jsonify({"erro": "Tarefa não encontrada"}), 404
    
    tarefa.toggle_status()
    return jsonify(tarefa.to_dict()), 200

# NOVA ROTA: Exportar tarefas para CSV
@app.route('/api/exportar')
def exportar_csv():
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Escreve o cabeçalho
    writer.writerow(['Título', 'Descrição', 'Data', 'Horário', 'Status'])
    
    # Escreve os dados das tarefas
    for tarefa in gerenciador._tarefas:
        if hasattr(tarefa, 'id'):
            data_formatada = tarefa._data_entrega.strftime('%d/%m/%Y')
            writer.writerow([tarefa.titulo, tarefa.descricao, data_formatada, tarefa._horario, tarefa.status])
            
    output.seek(0)
    
    response = make_response(output.getvalue())
    response.headers["Content-Disposition"] = "attachment; filename=tarefas.csv"
    response.headers["Content-type"] = "text/csv"
    
    return response

if __name__ == "__main__":
    popular_dados_iniciais()
    app.run(debug=True)
