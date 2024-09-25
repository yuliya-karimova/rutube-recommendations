<template>
    <div class="recommendations">
      <h2>Рекомендации</h2>
      <div v-for="video in videos" :key="video.id" class="video-item" @click="selectVideo(video)">
        <img :src="video.thumbnail" alt="Thumbnail" />
        <div>
          <h3>{{ video.title }}</h3>
          <p>{{ video.description }}</p>
        </div>
      </div>
    </div>
  </template>
  
  <script lang="ts" setup>
  import type { Video } from '../types'
  
  const props = defineProps<{
    videos: Video[]
  }>()
  
  const emit = defineEmits<{
    (e: 'video-selected', video: Video): void
  }>()
  
  const selectVideo = (video: Video) => {
    emit('video-selected', video)
  }
  </script>
  
  <style scoped>
  .recommendations {
    /* Стили для компонента */
  }
  .video-item {
    display: flex;
    cursor: pointer;
    margin-bottom: 10px;
  }
  .video-item img {
    width: 120px;
    height: 90px;
    margin-right: 10px;
  }
  </style>