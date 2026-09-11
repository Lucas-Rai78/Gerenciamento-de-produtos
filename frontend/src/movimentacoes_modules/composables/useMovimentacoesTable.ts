import type { Produto } from '@/produto_modules/types/produto'

interface UseMovimentacoesTableProps {
  produtos: Produto[]
}

export function useMovimentacoesTable(props: UseMovimentacoesTableProps) {
  function getNomeProduto(produtoId: number): string {
    const prod = props.produtos.find((p) => p.id === produtoId)
    return prod ? prod.nome : `Produto #${produtoId}`
  }

  return {
    getNomeProduto,
  }
}
