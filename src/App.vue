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
    <div class="py-8 px-4 xl:px-8">
      <div v-if="currentVideo" class="mb-4">
        <VideoCardFull :video="currentVideo" @react="onReact" />
      </div>
      <div ref="videoList" class="py-4">
        {{ currentVideo ? "Похожие видео:" : "Выберите понравившееся видео:" }}
      </div>
      <div>
        <div v-if="!isLoaded" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
          <div v-for="n in 10" :key="n" class="skeleton"></div>
        </div>
        <div
          v-else-if="recommendedVideos.length"
          class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4"
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
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted, nextTick } from "vue";
import VideoCard from "./components/VideoCard.vue";
import VideoCardFull from "./components/VideoCardFull.vue";
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
const isReactionSet = ref(false);

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
  if (currentVideo.value && !isReactionSet.value) {
    await onReact({ video_id: currentVideo.value.video_id, type: "dislike" });
    currentVideo.value = video;
    isReactionSet.value = false;
    return;
  }

  isReactionSet.value = false;
  currentVideo.value = video;
  isLoaded.value = false;
  try {
    scrollToTop();
    await fetchRelatedVideos(video.video_id);
  } catch (error) {
    console.log(error);
  } finally {
    isLoaded.value = true;
  }
};

const onReact = async (reaction: Reaction) => {
  isReactionSet.value = true;
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

<style scoped>
.skeleton {
  background-color: #1b273d;
  border-radius: 0.75rem;
  animation: pulse 1.5s infinite ease-in-out;
  height: 200px;
  width: 100%;
  margin-bottom: 16px;
}

@keyframes pulse {
  0% {
    background-color: #1b273d;
  }
  50% {
    background-color: #2f4060;
  }
  100% {
    background-color: #1b273d;
  }
}
</style>
