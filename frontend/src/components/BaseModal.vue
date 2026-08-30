<script setup lang="ts">
import { onMounted, onUnmounted } from 'vue'

defineProps<{
  isOpen: boolean
  title: string
}>()

const emit = defineEmits<{
  (e: 'close'): void
}>()

function handleKeyDown(event: KeyboardEvent) {
  if (event.key === 'Escape') {
    emit('close')
  }
}

onMounted(() => window.addEventListener('keydown', handleKeyDown))
onUnmounted(() => window.removeEventListener('keydown', handleKeyDown))
</script>

<template>
  <Teleport to="body">
    <div v-if="isOpen" class="modal-backdrop" @click.self="emit('close')">
      <div class="modal-container">
        <header class="modal-header">
          <h3>{{ title }}</h3>
          <button class="btn-close" @click="emit('close')">&times;</button>
        </header>
        <div class="modal-body">
          <slot />
        </div>
      </div>
    </div>
  </Teleport>
</template>

<style scoped>
.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
  padding: 1rem;
}

.modal-container {
  background: #ffffff;
  border-radius: 0.5rem;
  width: 100%;
  max-width: 650px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
  display: flex;
  flex-direction: column;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.25rem 1.5rem;
  border-bottom: 1px solid #e2e8f0;
}

.modal-header h3 {
  margin: 0;
  font-size: 1.2rem;
  color: #1e293b;
}

.btn-close {
  background: transparent;
  border: none;
  font-size: 1.75rem;
  line-height: 1;
  color: #64748b;
  cursor: pointer;
  padding: 0;
}

.btn-close:hover {
  color: #0f172a;
}

.modal-body {
  padding: 1.5rem;
}
</style>
