import { ref, onMounted } from 'vue'
import type {
  Produto,
  ProdutoCreate,
  Categoria,
  UnidadeMedida,
} from '@/produto_modules/types/produto'
import { produtoService } from '@/produto_modules/services/produtoService'

const CATEGORIAS: Categoria[] = ['não perecíveis', 'frezer', 'hortifruti', 'embalagens', 'bebidas']
const UNIDADES_MEDIDA: UnidadeMedida[] = ['g', 'kg', 'mL', 'L']

function criarFormVazio(): ProdutoCreate {
  return {
    nome: '',
    descricao: '',
    quantidadeEstoque: 0,
    estoqueMinimo: 0,
    precoUnidade: 0,
    peso: 'kg',
    categoria: 'não perecíveis',
  }
}

export function useProdutosView() {
  const categorias = CATEGORIAS
  const unidadesMedida = UNIDADES_MEDIDA

  const listaProdutos = ref<Produto[]>([])
  const carregando = ref<boolean>(false)
  const idEmEdicao = ref<number | null>(null)
  const isModalOpen = ref<boolean>(false)
  const form = ref<ProdutoCreate>(criarFormVazio())

  function resetForm(): void {
    form.value = criarFormVazio()
    idEmEdicao.value = null
    isModalOpen.value = false
  }

  function abrirModalNovo(): void {
    resetForm()
    isModalOpen.value = true
  }

  async function carregarProdutos(): Promise<void> {
    try {
      carregando.value = true
      listaProdutos.value = await produtoService.listar()
    } catch (error) {
      console.error('Falha na comunicação com o backend:', error)
    } finally {
      carregando.value = false
    }
  }

  async function salvarProduto(): Promise<void> {
    try {
      if (idEmEdicao.value) {
        await produtoService.atualizar(idEmEdicao.value, form.value)
      } else {
        await produtoService.criar(form.value)
      }
      resetForm()
      await carregarProdutos()
    } catch (error) {
      console.error('Erro ao salvar produto:', error)
    }
  }

  function prepararEdicao(prod: Produto): void {
    idEmEdicao.value = prod.id
    form.value = {
      nome: prod.nome,
      descricao: prod.descricao,
      quantidadeEstoque: prod.quantidadeEstoque,
      estoqueMinimo: prod.estoqueMinimo,
      precoUnidade: prod.precoUnidade,
      peso: prod.peso,
      categoria: prod.categoria,
    }
    isModalOpen.value = true
  }

  async function excluirProduto(id: number): Promise<void> {
    if (confirm('Tem certeza que deseja remover este produto?')) {
      try {
        await produtoService.deletar(id)
        await carregarProdutos()
      } catch (error) {
        alert(`Erro ao excluir: ${error instanceof Error ? error.message : String(error)}`)
      }
    }
  }

  onMounted(() => {
    carregarProdutos()
  })

  return {
    categorias,
    unidadesMedida,
    listaProdutos,
    carregando,
    idEmEdicao,
    isModalOpen,
    form,
    resetForm,
    abrirModalNovo,
    carregarProdutos,
    salvarProduto,
    prepararEdicao,
    excluirProduto,
  }
}
