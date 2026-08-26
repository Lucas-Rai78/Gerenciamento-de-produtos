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
  <div class="input-group">
    <label class="input-label">
      {{ label }}
      <span v-if="required" class="required-asterisk">*</span>
    </label>
    <input
      v-model="model"
      :type="type"
      :required="required"
      :step="step"
      :min="type === 'number' ? min : undefined"
      class="input-field"
    />
  </div>
</template>

<style scoped>
.input-group {
  display: flex;
  flex-direction: column;
  gap: 0.375rem;
  margin-bottom: 1rem;
}

.input-label {
  font-size: 0.875rem;
  font-weight: 600;
  color: #121212;
}

.required-asterisk {
  color: #ef4444;
}

.input-field {
  padding: 0.625rem 0.75rem;
  border: 1px solid #d4d4d4;
  border-radius: 0.375rem;
  font-size: 0.95rem;
  outline: none;
  transition: border-color 0.2s, box-shadow 0.2s;
}

.input-field:focus {
  border-color: #00bf63;
  box-shadow: 0 0 0 3px rgba(0, 191, 99, 0.15);
}
</style>
