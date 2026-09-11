import type { Produto } from '@/produto_modules/types/produto'

type Emits = {
  (e: 'editar', produto: Produto): void
  (e: 'excluir', id: number): void
}

export function useProdutoTable(emit: Emits) {
  function onEditar(produto: Produto): void {
    emit('editar', produto)
  }

  function onExcluir(id: number): void {
    emit('excluir', id)
  }

  return {
    onEditar,
    onExcluir,
  }
}
