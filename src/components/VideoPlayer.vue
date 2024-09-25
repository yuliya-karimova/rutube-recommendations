<template>
    <div class="video-player">
      <video
        ref="videoRef"
        :src="video.url"
        controls
        @timeupdate="onTimeUpdate"
        @pause="onPause"
        @play="onPlay"
        @ended="onEnded"
      ></video>
      <div class="video-info">
        <h3>{{ video.title }}</h3>
        <p>{{ video.description }}</p>
      </div>
    </div>
  </template>
  
  <script lang="ts" setup>
  import { ref, onMounted } from 'vue'
  import type { Video } from '../types'
  
  const props = defineProps<{
    video: Video
    onInteraction: (interaction: Interaction) => void
  }>()
  
  const videoRef = ref<HTMLVideoElement | null>(null)
  const watchStartTime = ref<number>(0)
  
  const onTimeUpdate = () => {
    if (videoRef.value) {
      const currentTime = videoRef.value.currentTime
      watchStartTime.value = currentTime
    }
  }
  
  const onPause = () => {
    emitInteraction('pause')
  }
  
  const onPlay = () => {
    emitInteraction('play')
  }
  
  const onEnded = () => {
    emitInteraction('ended')
  }
  
  const emitInteraction = (type: string) => {
    const interaction: Interaction = {
      videoId: props.video.id,
      type,
      timestamp: Date.now(),
    }
    props.onInteraction(interaction)
  }
  </script>
  
  <style scoped>
  .video-player {
    /* Стили для компонента */
  }
  </style>