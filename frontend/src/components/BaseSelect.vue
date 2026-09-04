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
  <div class="flex flex-col gap-1.5 mb-1">
    <label class="text-sm text-gray-900 ">
      {{ label }}
      <span v-if="required" class="text-red-500">*</span>
    </label>
    <select v-model="model" :required="required" class="px-3! py-2.5! border border-neutral-300 rounded-md text-1 bg-white outline-none transition-[border-color,box-shadow] duration-200 focus:border-[#00bf63] focus:ring-4 focus:ring-[#00bf63]/15">
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
