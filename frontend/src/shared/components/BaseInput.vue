<script setup lang="ts">
interface Props {
  label: string;
  type?: 'text' | 'number' | 'date';
  required?: boolean;
  step?: string;
  min?: number;
}

withDefaults(defineProps<Props>(), {
  type: 'text',
  required: false,
  step: 'any',
  min: 0,
});

const model = defineModel<string | number>({ required: true });
</script>

<template>
  <div class="flex flex-col gap-1.5 mb-1">
    <label class="text-sm text-gray-900">
      {{ label }}
      <span v-if="required" class="text-red-500">*</span>
    </label>
    <input
      v-model="model"
      :type="type"
      :required="required"
      :step="step"
      :min="type === 'number' ? min : undefined"
      class="px-3! py-2.5! border border-neutral-300 rounded-md text-1 outline-none transition-[border-color,box-shadow] duration-200 focus:border-[#00bf63] focus:ring-4 focus:ring-[#00bf63]/15"
    />
  </div>
</template>
