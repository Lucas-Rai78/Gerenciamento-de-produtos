export type UnidadeMedida = 'g' | 'kg' | 'mL' | 'L'
export type MotivoSaida = 'venda' | 'descarte' | 'producao'
export type Categoria =  'não perecíveis' | 'frezer' | 'hortifruti' | 'embalagens' | 'bebidas'
export type Classificacao = 'compra' | 'producao'

export interface ProdutoBase {
  nome: string
  descricao: string
  quantidadeEstoque: number
  estoqueMinimo: number
  precoUnidade: number
  peso: UnidadeMedida
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

export type ProdutoCreate = ProdutoBase;

export interface Produto extends ProdutoBase {
  id: number;
}
