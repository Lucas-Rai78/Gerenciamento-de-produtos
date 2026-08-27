import type { EntradaProduto, SaidaProduto } from '@/types/produto';

const API_BASE = 'http://127.0.0.1:8000';

export const movimentacaoService = {
  async listarEntradas(): Promise<EntradaProduto[]> {
    const res = await fetch(`${API_BASE}/entradas/`);
    if (!res.ok) throw new Error('Erro ao buscar entradas');
    return res.json();
  },

  async criarEntrada(entrada: Omit<EntradaProduto, 'id'>): Promise<EntradaProduto> {
    const res = await fetch(`${API_BASE}/entradas/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(entrada),
    });
    if (!res.ok) throw new Error('Erro ao registrar entrada');
    return res.json();
  },

  async listarSaidas(): Promise<SaidaProduto[]> {
    const res = await fetch(`${API_BASE}/saidas/`);
    if (!res.ok) throw new Error('Erro ao buscar saídas');
    return res.json();
  },

  async criarSaida(saida: Omit<SaidaProduto, 'id'>): Promise<SaidaProduto> {
    const res = await fetch(`${API_BASE}/saidas/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(saida),
    });
    if (!res.ok) throw new Error('Erro ao registrar saída');
    return res.json();
  },
};
