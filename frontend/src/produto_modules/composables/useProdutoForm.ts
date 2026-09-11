type Emits = {
  (e: 'salvar'): void
  (e: 'cancelar'): void
}

export function useProdutoForm(emit: Emits) {
  function onSalvar(): void {
    emit('salvar')
  }

  function onCancelar(): void {
    emit('cancelar')
  }

  return {
    onSalvar,
    onCancelar,
  }
}
c
