const API_URL = "http://127.0.0.1:8000/produtos/";

document.addEventListener("DOMContentLoaded", carregarProdutos);

document.getElementById("form-produto").addEventListener("submit", async (event) => {
    event.preventDefault();

    const id = document.getElementById("produto-id").value;

    const produtoData = {
        nome: document.getElementById("nome").value,
        preco: parseFloat(document.getElementById("preco").value),
        peso: parseFloat(document.getElementById("peso").value),
        validade: document.getElementById("validade").value,
        descricao: document.getElementById("descricao").value
    };

    const url = id ? `${API_URL}${id}` : API_URL;
    const method = id ? "PUT" : "POST";

    const resposta = await fetch(url, {
        method: method,
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(produtoData)
    });

    if (resposta.ok) {
        limparFormulario();
        carregarProdutos();
    } else {
        alert(`Erro ao ${id ? "atualizar" : "cadastrar"} produto.`);
    }
});

async function carregarProdutos() {
    const resposta = await fetch(API_URL);
    const produtos = await resposta.json();

    const listaContainer = document.getElementById("lista-produtos");
    listaContainer.innerHTML = "";

    produtos.forEach(produto => {
        const card = document.createElement("div");
        card.classList.add("card");

        card.innerHTML = `
            <h3>${produto.nome}</h3>
            <div class="preco">R$ ${produto.preco.toFixed(2)}</div>
            <p><strong>Descrição:</strong> ${produto.descricao}</p>
            <p><strong>Peso:</strong> ${produto.peso} g</p>
            <p><strong>Validade:</strong> ${produto.validade}</p>
            <div>
                <button class="btn-editar" onclick="prepararEdicao(${JSON.stringify(produto).replace(/"/g, '&quot;')})">Editar</button>
                <button class="btn-deletar" onclick="deletarProduto(${produto.id})">Excluir</button>
            </div>
        `;

        listaContainer.appendChild(card);
    });
}

// Preenche o formulário com os dados do produto clicado para edição
function prepararEdicao(produto) {
    document.getElementById("produto-id").value = produto.id;
    document.getElementById("nome").value = produto.nome;
    document.getElementById("preco").value = produto.preco;
    document.getElementById("peso").value = produto.peso;
    document.getElementById("validade").value = produto.validade;
    document.getElementById("descricao").value = produto.descricao;

    // Altera interface para o modo de edição
    document.getElementById("form-titulo").innerText = "Editar Produto";
    document.getElementById("btn-submit").innerText = "Salvar Alterações";
    document.getElementById("btn-submit").style.backgroundColor = "#f39c12";
    document.getElementById("btn-cancelar").style.display = "block";

    window.scrollTo({ top: 0, behavior: 'smooth' });
}

function limparFormulario() {
    document.getElementById("produto-id").value = "";
    document.getElementById("form-produto").reset();
    
    document.getElementById("form-titulo").innerText = "Cadastrar Novo Produto";
    document.getElementById("btn-submit").innerText = "Cadastrar Produto";
    document.getElementById("btn-submit").style.backgroundColor = "#27ae60";
    document.getElementById("btn-cancelar").style.display = "none";
}

async function deletarProduto(id) {
    if (confirm("Tem certeza que deseja excluir este produto?")) {
        const resposta = await fetch(`${API_URL}${id}`, {
            method: "DELETE"
        });

        if (resposta.ok) {
            carregarProdutos();
        } else {
            alert("Erro ao deletar o produto.");
        }
    }
}