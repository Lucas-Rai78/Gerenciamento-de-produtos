import { onMounted, onUnmounted } from 'vue'

export function useEscapeKey(onEscape: () => void) {
  function handleKeyDown(event: KeyboardEvent): void {
    if (event.key === 'Escape') {
      onEscape()
    }
  }

  onMounted(() => window.addEventListener('keydown', handleKeyDown))
  onUnmounted(() => window.removeEventListener('keydown', handleKeyDown))
}
