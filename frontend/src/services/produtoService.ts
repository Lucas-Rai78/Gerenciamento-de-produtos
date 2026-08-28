import type { Produto, ProdutoCreate } from '@/types/produto'

const API_BASE = 'http://127.0.0.1:8000'

export const produtoService = {
  async listar(): Promise<Produto[]> {
    const response = await fetch(`${API_BASE}/produtos/`)
    if (!response.ok) throw new Error('Erro ao buscar produtos')
    return response.json()
  },

  async buscarPorId(id: number): Promise<Produto> {
    const response = await fetch(`${API_BASE}/produtos/${id}`)
    if (!response.ok) throw new Error('Produto não encontrado')
    return response.json()
  },

  async criar(produto: ProdutoCreate): Promise<Produto> {
    const response = await fetch(`${API_BASE}/produtos/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(produto),
    })
    if (!response.ok) throw new Error('Erro ao cadastrar produto')
    return response.json()
  },

  async atualizar(id: number, produto: ProdutoCreate): Promise<Produto> {
    const response = await fetch(`${API_BASE}/produtos/${id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(produto),
    })
    if (!response.ok) throw new Error('Erro ao atualizar produto')
    return response.json()
  },

  async deletar(id: number): Promise<void> {
    const res = await fetch(`${API_BASE}/produtos/${id}`, {
      method: 'DELETE',
    })

    if (!res.ok) {
      const err: { detail?: string } = await res.json()
      throw new Error(err.detail || 'Erro ao excluir produto no servidor.')
    }
  },
}
