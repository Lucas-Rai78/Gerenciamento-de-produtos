export type UnidadeMedida = 'g' | 'kg' | 'mL' | 'L'
export type MotivoSaida = 'venda' | 'descarte' | 'producao'
export type Categoria = 'estoque seco' | 'doce'
export type Classificacao = 'compra' | 'producao'

export interface Produto {
  id?: string
  nome: string
  descricao?: string
  quantidadeEstoque: number
  estoqueMinimo: number
  precoUnidade: number
  categoria: Categoria
}

export interface EntradaProduto {
  id: string
  produtoId: string
  classificacao: Classificacao
  unidadeMedida: UnidadeMedida
  quantidade: number
  precoUnitario: number
  dataEntrada: string
  validade?: string
}

export interface SaidaProduto {
  id: string
  produtoId: string
  motivo: MotivoSaida
  unidadeMedida: UnidadeMedida
  quantidade: number
  dataSaida: string
}
