<script setup lang="ts" generic="T extends string">
interface Option<V> {
  label: string;
  value: V;
}

interface Props {
  label: string;
  options: Option<T>[] | readonly T[];
  required?: boolean;
  placeholder?: string;
}

withDefaults(defineProps<Props>(), {
  required: false,
  placeholder: 'Selecione uma opção'
});

const model = defineModel<T>({ required: true });
</script>

<template>
  <div class="select-group">
    <label class="select-label">
      {{ label }}
      <span v-if="required" class="required-asterisk">*</span>
    </label>
    <select v-model="model" :required="required" class="select-field">
      <option value="" disabled selected>{{ placeholder }}</option>
      <option
        v-for="opt in options"
        :key="typeof opt === 'string' ? opt : opt.value"
        :value="typeof opt === 'string' ? opt : opt.value"
      >
        {{ typeof opt === 'string' ? opt : opt.label }}
      </option>
    </select>
  </div>
</template>

<style scoped>
.select-group {
  display: flex;
  flex-direction: column;
  gap: 0.375rem;
  margin-bottom: 1rem;
}

.select-label {
  font-size: 0.875rem;
  font-weight: 600;
  color: #334155;
}

.required-asterisk {
  color: #ef4444;
}

.select-field {
  padding: 0.625rem 0.75rem;
  border: 1px solid #cbd5e1;
  border-radius: 0.375rem;
  font-size: 0.95rem;
  background-color: #ffffff;
  outline: none;
  transition: border-color 0.2s, box-shadow 0.2s;
}

.select-field:focus {
  border-color: #2563eb;
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.15);
}
</style>