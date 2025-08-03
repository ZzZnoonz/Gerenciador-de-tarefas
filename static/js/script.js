document.addEventListener('DOMContentLoaded', () => {
    // --- SELETORES DE ELEMENTOS ---
    const formCriacao = document.getElementById('form-nova-tarefa');
    const listaTarefasUL = document.getElementById('lista-tarefas');
    const modalEdicao = document.getElementById('modal-edicao');
    const formEdicao = document.getElementById('form-edicao');
    const closeButton = document.querySelector('.close-button');
    const btnExportar = document.getElementById('btn-exportar');

    // --- FUNÇÕES DE API ---
    async function carregarTarefas() {
        try {
            const response = await fetch('/api/tarefas');
            if (!response.ok) throw new Error('Falha ao carregar tarefas');
            const tarefas = await response.json();
            renderizarTarefas(tarefas);
        } catch (error) {
            console.error('Erro:', error);
        }
    }

    async function criarTarefa(dados) {
        try {
            await fetch('/api/tarefas', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(dados),
            });
            carregarTarefas();
        } catch (error) {
            console.error('Erro:', error);
        }
    }

    async function atualizarTarefa(id, dados) {
        try {
            await fetch(`/api/tarefas/${id}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(dados),
            });
            carregarTarefas();
            fecharModal();
        } catch (error) {
            console.error('Erro:', error);
        }
    }

    async function deletarTarefa(id) {
        if (confirm('Tem certeza que deseja excluir esta tarefa?')) {
            try {
                await fetch(`/api/tarefas/${id}`, { method: 'DELETE' });
                carregarTarefas();
            } catch (error) {
                console.error('Erro:', error);
            }
        }
    }

    async function toggleStatus(id) {
        try {
            await fetch(`/api/tarefas/${id}/toggle-status`, { method: 'POST' });
            carregarTarefas();
        } catch (error) {
            console.error('Erro:', error);
        }
    }

    // --- FUNÇÃO DE RENDERIZAÇÃO ---
    function renderizarTarefas(tarefas) {
        listaTarefasUL.innerHTML = '';
        tarefas.forEach(tarefa => {
            const li = document.createElement('li');
            const [ano, mes, dia] = tarefa.data_entrega.split('-');
            const dataFormatada = `${dia}/${mes}/${ano}`;
            const statusClass = tarefa.status === 'Concluído' ? 'status-concluido' : 'status-pendente';

            li.innerHTML = `
                <span class="col-titulo">${tarefa.titulo}</span>
                <span class="col-descricao">${tarefa.descricao}</span>
                <span class="col-data">${dataFormatada} às ${tarefa.horario}</span>
                <div class="col-status">
                    <button class="status-btn ${statusClass}" data-id="${tarefa.id}">
                        ${tarefa.status}
                    </button>
                </div>
                <div class="col-acoes">
                    <button class="edit-btn" data-id="${tarefa.id}">Editar</button>
                    <button class="delete-btn" data-id="${tarefa.id}">Excluir</button>
                </div>
            `;
            listaTarefasUL.appendChild(li);
        });
    }

    // --- FUNÇÕES DE MODAL ---
    function abrirModal(tarefa) {
        document.getElementById('edit-id').value = tarefa.id;
        document.getElementById('edit-titulo').value = tarefa.titulo;
        document.getElementById('edit-descricao').value = tarefa.descricao;
        document.getElementById('edit-data').value = tarefa.data_entrega;
        document.getElementById('edit-horario').value = tarefa.horario;
        modalEdicao.style.display = 'block';
    }

    function fecharModal() {
        modalEdicao.style.display = 'none';
    }

    // --- EVENT LISTENERS ---
    formCriacao.addEventListener('submit', (event) => {
        event.preventDefault();
        const dados = {
            titulo: document.getElementById('input-titulo-tarefa').value,
            descricao: document.getElementById('input-descricao-tarefa').value,
            data_entrega: document.getElementById('input-data-tarefa').value,
            horario: document.getElementById('input-horario-tarefa').value,
        };
        criarTarefa(dados);
        formCriacao.reset();
    });

    formEdicao.addEventListener('submit', (event) => {
        event.preventDefault();
        const id = document.getElementById('edit-id').value;
        const dados = {
            titulo: document.getElementById('edit-titulo').value,
            descricao: document.getElementById('edit-descricao').value,
            data_entrega: document.getElementById('edit-data').value,
            horario: document.getElementById('edit-horario').value,
        };
        atualizarTarefa(id, dados);
    });

    listaTarefasUL.addEventListener('click', async (event) => {
        const target = event.target;
        const id = target.dataset.id;
        if (target.classList.contains('delete-btn')) deletarTarefa(id);
        if (target.classList.contains('status-btn')) toggleStatus(id);
        if (target.classList.contains('edit-btn')) {
            const response = await fetch('/api/tarefas');
            const tarefas = await response.json();
            const tarefaParaEditar = tarefas.find(t => t.id == id);
            if (tarefaParaEditar) abrirModal(tarefaParaEditar);
        }
    });

    btnExportar.addEventListener('click', () => {
        window.location.href = '/api/exportar';
    });

    closeButton.addEventListener('click', fecharModal);
    window.addEventListener('click', (event) => {
        if (event.target == modalEdicao) fecharModal();
    });

    carregarTarefas();
});
