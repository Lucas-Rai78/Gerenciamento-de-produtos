import type { UnidadeMedida } from '@/shared/types/globalTypes'

export type { UnidadeMedida }
export type Categoria = 'não perecíveis' | 'frezer' | 'hortifruti' | 'embalagens' | 'bebidas'

export interface ProdutoBase {
  nome: string
  descricao: string
  quantidadeEstoque: number
  estoqueMinimo: number
  precoUnidade: number
  peso: UnidadeMedida
  categoria: Categoria
}

export type ProdutoCreate = ProdutoBase

export interface Produto extends ProdutoBase {
  id: number
}
