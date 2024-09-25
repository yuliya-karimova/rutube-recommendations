<template>
    <div class="interest-selector">
      <h2>Выберите ваши интересы</h2>
      <div v-for="interest in availableInterests" :key="interest">
        <input type="checkbox" :id="interest" :value="interest" v-model="selectedInterests" />
        <label :for="interest">{{ interest }}</label>
      </div>
      <button @click="submitInterests">Подтвердить</button>
    </div>
  </template>
  
  <script lang="ts" setup>
  import { ref } from 'vue'
  
  const props = defineProps<{
    availableInterests: string[]
  }>()
  
  const emit = defineEmits<{
    (e: 'interests-selected', interests: string[]): void
  }>()
  
  const selectedInterests = ref<string[]>([])
  
  const submitInterests = () => {
    emit('interests-selected', selectedInterests.value)
  }
  </script>
  
  <style scoped>
  .interest-selector {
    /* Стили для компонента */
  }
  </style>