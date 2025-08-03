# services/gerenciador.py
import csv
from typing import List, Optional
from models.tarefa import Tarefa
from models.usuario import Usuario
from interfaces.exportavel import Exportavel

# A classe Gerenciador implementa a interface Exportavel[Tarefa]
class Gerenciador(Exportavel[Tarefa]):
    """
    Gerencia as tarefas e usuários do sistema.
    Implementa a interface Exportavel para poder exportar a lista de tarefas.
    """
    def __init__(self):
        self._tarefas: List[Tarefa] = []
        self._usuarios: List[Usuario] = []

    def adicionar_tarefa(self, tarefa: Tarefa):
        self._tarefas.append(tarefa)

    def listar_tarefas(self):
        if not self._tarefas:
            print("Nenhuma tarefa cadastrada.")
            return
        for tarefa in self._tarefas:
            print(tarefa.exibir_detalhes())
            print("-" * 20)

    # --- SOBRECARGA DE MÉTODOS (Simulação em Python) ---
    def buscar_tarefa(self, termo: str, status: Optional[str] = None) -> List[Tarefa]:
        """
        Busca tarefas pelo título. Se o status for fornecido, filtra também por status.
        Isso simula a sobrecarga de métodos, onde a mesma função se comporta
        de forma diferente com base nos argumentos passados.
        """
        resultados = [t for t in self._tarefas if termo.lower() in t.titulo.lower()]
        if status:
            resultados = [t for t in resultados if t.status.lower() == status.lower()]
        return resultados

    # --- Implementação do método da Interface Exportavel ---
    def exportar(self, dados: List[Tarefa], nome_arquivo: str) -> bool:
        """
        Exporta a lista de tarefas para um arquivo CSV.
        """
        if not nome_arquivo.endswith('.csv'):
            nome_arquivo += '.csv'

        try:
            with open(nome_arquivo, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                # Escreve o cabeçalho
                writer.writerow(['Tipo', 'Titulo', 'Status', 'Detalhes'])

                for tarefa in dados:
                    # Usando type() para diferenciar as tarefas
                    tipo = type(tarefa).__name__
                    detalhes = ""
                    # Acessamos atributos específicos após checar o tipo
                    if isinstance(tarefa, TarefaSimples):
                        detalhes = tarefa._data_entrega.strftime('%d/%m/%Y')
                    elif isinstance(tarefa, TarefaComposta):
                        detalhes = f"{len(tarefa._subtarefas)} subtarefas"

                    writer.writerow([tipo, tarefa.titulo, tarefa.status, detalhes])
            print(f"Dados exportados com sucesso para {nome_arquivo}")
            return True
        except IOError as e:
            print(f"Erro ao exportar arquivo: {e}")
            return False