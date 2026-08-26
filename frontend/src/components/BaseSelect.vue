<script setup lang="ts" generic="T extends string">
interface Option<V> {
  label: string;
  value: V;
}

interface Props {
  label: string;
  options: Option<T>[] | readonly T[];
  required?: boolean;
}

withDefaults(defineProps<Props>(), {
  required: false,
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
      <option value="" disabled selected></option>
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
  color: #121212;
}

.required-asterisk {
  color: #ef4444;
}

.select-field {
  padding: 0.625rem 0.75rem;
  border: 1px solid #d4d4d4;
  border-radius: 0.375rem;
  font-size: 0.95rem;
  background-color: #ffffff;
  outline: none;
  transition: border-color 0.2s, box-shadow 0.2s;
}

.select-field:focus {
  border-color: #00bf63;
  box-shadow: 0 0 0 3px rgba(0, 191, 99, 0.15);
}
</style>
