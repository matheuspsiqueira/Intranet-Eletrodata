/* SERVICE STATUS */

// FLUIG

async function atualizarStatus() {
  try {
    // Faz requisição para sua view Django que retorna o status em JSON
    const response = await fetch('/api/status_servicos'); 
    const status = await response.json();

    // Atualiza cada item na lista
    document.querySelectorAll('#servicos-lista li').forEach(li => {
      const servico = li.dataset.servico;
      if (status[servico]) {
        li.querySelector('.status').textContent = status[servico].texto;
        li.querySelector('.status').className = 'status ' + status[servico].classe;
      }
    });
  } catch (err) {
    console.error('Erro ao atualizar status:', err);
  }
}

// Atualiza imediatamente e depois a cada 60 segundos
atualizarStatus();
setInterval(atualizarStatus, 60000);


