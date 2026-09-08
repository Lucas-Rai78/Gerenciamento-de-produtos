const API_BASE = 'http://127.0.0.1:8000';

export interface Movimentacao {
  id?: number;
  produto_id: number;
  tipo: 'entrada' | 'saida';
  categoriaMovimentacao: string;
  unidadeMedida: string;
  quantidade: number;
  precoUnitario?: number;
  data: string;
  validade?: string | null;
}

export const movimentacaoService = {
  async listar(): Promise<Movimentacao[]> {
    const res = await fetch(`${API_BASE}/movimentacoes/`);
    if (!res.ok) throw new Error('Erro ao buscar movimentações');
    return res.json();
  },

  async criar(movimentacao: Movimentacao): Promise<Movimentacao> {
    const res = await fetch(`${API_BASE}/movimentacoes/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(movimentacao),
    });
    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.detail || 'Erro ao registrar movimentação');
    }
    return res.json();
  },
};
