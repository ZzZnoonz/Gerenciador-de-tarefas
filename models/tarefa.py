from abc import ABC, abstractmethod
from datetime import date
from typing import List
import time

# --- CLASSE ABSTRATA TAREFA (PAI) ---
class Tarefa(ABC):
    def __init__(self, titulo: str, descricao: str):
        # ATUALIZAÇÃO: O segundo parâmetro agora é a descrição geral
        self._titulo = titulo
        self._descricao = descricao
        self._status = "Pendente"

    @property
    def titulo(self) -> str:
        return self._titulo

    @property
    def descricao(self) -> str:
        return self._descricao

    @property
    def status(self) -> str:
        return self._status

    # NOVO: Método para alternar o status
    def toggle_status(self):
        """Alterna o status entre 'Pendente' e 'Concluído'."""
        if self._status == "Pendente":
            self._status = "Concluído"
        else:
            self._status = "Pendente"

    @abstractmethod
    def to_dict(self) -> dict:
        """Converte o objeto para um dicionário compatível com JSON."""
        pass

# --- CLASSE TAREFA SIMPLES (FILHA) ---
class TarefaSimples(Tarefa):
    """Representa uma tarefa com data, horário e um ID único."""
    def __init__(self, titulo: str, descricao: str, data_entrega: date, horario: str):
        # ATUALIZAÇÃO: O campo 'responsavel' foi removido do construtor
        super().__init__(titulo, descricao)
        self._data_entrega = data_entrega
        self._horario = horario
        self.id = int(time.time() * 1000)

    def to_dict(self) -> dict:
        """Converte o objeto para um dicionário para ser enviado ao frontend."""
        return {
            "id": self.id,
            "tipo": "Simples",
            "titulo": self.titulo,
            "descricao": self.descricao, # ATUALIZAÇÃO: Usa a descrição da classe pai
            "status": self.status,
            "data_entrega": self._data_entrega.strftime('%Y-%m-%d'),
            "horario": self._horario,
        }

# --- CLASSE TAREFA COMPOSTA (FILHA) ---
# Mantida para consistência do modelo, embora não usada na UI principal.
class TarefaComposta(Tarefa):
    def __init__(self, titulo: str, descricao: str):
        super().__init__(titulo, descricao)
        self._subtarefas: List[Tarefa] = []

    def adicionar_subtarefa(self, subtarefa: Tarefa):
        self._subtarefas.append(subtarefa)

    def to_dict(self) -> dict:
        return {
            "tipo": "Composta",
            "titulo": self.titulo,
            "descricao": self.descricao,
            "status": self.status,
            "subtarefas": [sub.to_dict() for sub in self._subtarefas]
        }