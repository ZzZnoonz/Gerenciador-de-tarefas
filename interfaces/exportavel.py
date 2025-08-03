# interfaces/exportavel.py
from abc import ABC, abstractmethod
from typing import List, TypeVar, Generic

# T é uma variável de tipo genérico. Pode ser qualquer tipo.
# Isso torna nossa interface reutilizável para exportar listas de qualquer coisa.
T = TypeVar('T')

class Exportavel(ABC, Generic[T]):
    """
    Define o contrato para classes que podem exportar uma lista de dados
    para um formato específico (ex: CSV, JSON).
    O uso de Generic[T] e TypeVar torna esta interface genérica.
    """

    @abstractmethod
    def exportar(self, dados: List[T], nome_arquivo: str) -> bool:
        """
        Método abstrato para exportar uma lista de dados.

        Args:
            dados (List[T]): Uma lista de objetos do tipo T para exportar.
            nome_arquivo (str): O nome do arquivo a ser gerado (ex: 'tarefas.csv').

        Returns:
            bool: True se a exportação foi bem-sucedida, False caso contrário.
        """
        pass