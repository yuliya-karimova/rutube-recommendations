<template>
  <div id="app">
    <div class="bg-gray-800 py-6 px-4 xl:px-8 flex flex-col gap-2 items-center">
      <div class="w-48 xl:w-64 text-white">
        <img src="./assets/rutube.svg" />
      </div>
      <div class="text-lg uppercase font-bold text-center">
        Сервис подбора рекомендаций
      </div>
    </div>
    <div class="py-8 px-4 xl:px-8 flex flex-col gap-4">
      <div v-if="currentVideo" class="mb-8">
        <VideoCardFull :video="currentVideo" @react="onReact" />
      </div>
      <div>
        {{ currentVideo ? "Похожие видео:" : "Выберите понравившееся видео:" }}
      </div>
      <div ref="videoList">
        <BaseSpinner v-if="!isLoaded" />
        <div
          v-else-if="recommendedVideos.length"
          class="grid grid-cols-2 xl:grid-cols-3 gap-4"
        >
          <VideoCard
            v-for="video in recommendedVideos"
            :key="video.video_id"
            :video="video"
            class="cursor-pointer"
            @click="() => onSelect(video)"
          />
        </div>
      </div>
      <!-- <VideoCard
        v-if="currentVideo"
        :video="currentVideo"
        @Reaction="onReaction"
      />
      <Recommendations
        :videos="recommendedVideos"
        @video-selected="onVideoSelected"
      />
      <button @click="toggleReactionsLog" class="mt-4">
        Показать/Скрыть Лог Взаимодействий
      </button>
      <div v-if="showReactionsLog" class="Reactions-log">
        <h3>Лог Взаимодействий</h3>
        <pre>{{ Reactions }}</pre>
      </div> -->
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted, nextTick } from "vue";
import VideoCard from "./components/VideoCard.vue";
import VideoCardFull from "./components/VideoCardFull.vue";
import BaseSpinner from "./components/BaseSpinner.vue";
import { useRecommendations } from "./composables/useRecommendations";
import type { Video, Reaction } from "./types";

const {
  recommendedVideos,
  fetchInitialVideos,
  fetchRecommendedVideos,
  fetchRelatedVideos,
} = useRecommendations();

const currentVideo = ref<Video | null>(null);
const isLoaded = ref(false);
const videoList = ref<HTMLElement | null>(null);

const scrollToVideos = () => {
  nextTick(() => {
    if (videoList.value) {
      videoList.value.scrollIntoView({
        behavior: "smooth",
      });
    }
  });
};

const scrollToTop = () => {
  nextTick(() => {
    window.scrollTo({
      top: 0, // Прокручиваем к верху страницы
      behavior: "smooth", // Плавная прокрутка
    });
  });
};

const onSelect = async (video: Video) => {
  currentVideo.value = video;
  isLoaded.value = false;
  try {
    await fetchRelatedVideos(video.video_id);
    scrollToTop()
  } catch (error) {
    console.log(error);
  } finally {
    isLoaded.value = true;
  }
};

const onReact = async (reaction: Reaction) => {
  isLoaded.value = false;
  try {
    await fetchRecommendedVideos(reaction);
    scrollToVideos();
  } catch (error) {
    console.log(error);
  } finally {
    isLoaded.value = true;
  }
};

const load = async () => {
  isLoaded.value = false;
  try {
    await fetchInitialVideos();
  } catch (error) {
    console.log(error);
  } finally {
    isLoaded.value = true;
  }
};

onMounted(() => {
  load();
});
</script>
