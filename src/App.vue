<template>
  <div id="app">
    <InterestSelector
      v-if="!hasSelectedInterests"
      :availableInterests="availableInterests"
      @interests-selected="onInterestsSelected"
    />
    <div v-else>
      <VideoPlayer v-if="currentVideo" :video="currentVideo" @interaction="onInteraction" />
      <Recommendations :videos="recommendedVideos" @video-selected="onVideoSelected" />
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import InterestSelector from './components/InterestSelector.vue'
import VideoPlayer from './components/VideoPlayer.vue'
import Recommendations from './components/Recommendations.vue'
import { useRecommendations } from './composables/useRecommendations'
import type { Video, Interaction } from './types'

const availableInterests = ['Технологии', 'Музыка', 'Спорт', 'Кино', 'Наука']

const {
  userInterests,
  recommendedVideos,
  initializeRecommendations,
  handleInteraction,
} = useRecommendations()

const hasSelectedInterests = ref(false)
const currentVideo = ref<Video | null>(null)

const onInterestsSelected = (interests: string[]) => {
  initializeRecommendations(interests)
  hasSelectedInterests.value = true
  if (recommendedVideos.value.length > 0) {
    currentVideo.value = recommendedVideos.value[0]
  }
}

const onInteraction = (interaction: Interaction) => {
  handleInteraction(interaction)
}

const onVideoSelected = (video: Video) => {
  currentVideo.value = video
}
</script>

<style>
/* Глобальные стили */
#app {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}
</style>