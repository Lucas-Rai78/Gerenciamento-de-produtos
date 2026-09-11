<script setup lang="ts">
import { useEscapeKey } from '@/shared/composables/useEscapeKey'

defineProps<{
  isOpen: boolean
  title: string
}>()

const emit = defineEmits<{
  (e: 'close'): void
}>()

useEscapeKey(() => emit('close'))
</script>

<template>
  <Teleport to="body">
    <div
      v-if="isOpen"
      class="fixed inset-0 flex items-center justify-center z-9999 p-4 w-screen h-screen bg-black/50"
      @click.self="emit('close')"
    >
      <div
        class="bg-white rounded-lg w-full max-w-162.5 max-h-[90vh] overflow-y-auto shadow-2xl flex flex-col"
      >
        <header class="flex justify-between items-center px-6! py-5! border-b border-gray-100">
          <h3 class="m-0 text-[1.2rem] text-gray-900">{{ title }}</h3>
          <button
            class="bg-transparent border-none text-[1.75rem] leading-none text-gray-400 cursor-pointer p-0 hover:text-[#0f172a]"
            @click="emit('close')"
          >
            &times;
          </button>
        </header>
        <div class="p-6!">
          <slot />
        </div>
      </div>
    </div>
  </Teleport>
</template>
