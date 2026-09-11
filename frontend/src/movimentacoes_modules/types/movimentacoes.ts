import type { UnidadeMedida } from '@/shared/types/globalTypes'

export type MotivoSaida = 'venda' | 'descarte' | 'producao'
export type Classificacao = 'compra' | 'producao'

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
