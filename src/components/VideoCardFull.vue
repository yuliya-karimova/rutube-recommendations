<template>
  <div class="text-xs space-y-4">
    <div class="aspect-video bg-gray-300"></div>
    <div class="font-bold text-base pt-2">{{ video.title }}</div>
    <div class="flex gap-2 items-center text-base font-light">
      <button
        class="text-white flex items-center gap-1 cursor-pointer px-2 py-1 rounded-lg transition duration-150"
        :class="userReaction === 'like' && 'bg-gray-700'"
        @click="emitReaction('like')"
      >
        <img src="../assets/like.svg" class="w-6" />
        <div v-if="likes">{{ likes }}</div>
      </button>
      <button
        class="text-white flex items-center gap-1 cursor-pointer px-2 py-1 rounded-lg transition duration-150"
        :class="userReaction === 'dislike' && 'bg-gray-700'"
        @click="emitReaction('dislike')"
      >
        <img src="../assets/dislike.svg" class="w-6" />
        <div v-if="dislikes">{{ dislikes }}</div>
      </button>
    </div>
    <div class="space-y-4">
      <div class="text-gray-500">
        {{ video.description }}
      </div>
      <div class="space-y-1">
        <div>Категория: {{ video.category_id }}</div>
        <div>Опубликовано: {{ formattedDate }}</div>
        <div>Просмотры: {{ video.v_year_views }}</div>
        <div>Комментарии: {{ video.v_total_comments }}</div>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { computed, ref } from "vue";

import dayjs from "dayjs";
import type { Video, Reaction, ReactionType } from "../types";

const props = defineProps<{
  video: Video;
}>();
const emits = defineEmits(["react"]);

const likes = ref(props.video.v_likes);
const dislikes = ref(props.video.v_dislikes);
const userReaction = ref<ReactionType | null>(null);

const formattedDate = computed(() => {
  return props.video.v_pub_datetime
    ? dayjs(props.video.v_pub_datetime).format("YYYY-MM-DD")
    : "";
});

const emitReaction = (type: ReactionType) => {
  if (type === "like") {
    if (userReaction.value === "like") {
      likes.value -= 1;
    } else if (userReaction.value === "dislike") {
      likes.value += 1;
      dislikes.value -= 1;
    } else {
      likes.value += 1;
    }
  } else if (type === "dislike") {
    if (userReaction.value === "like") {
      likes.value -= 1;
      dislikes.value += 1;
    } else if (userReaction.value === "dislike") {
      dislikes.value -= 1;
    } else {
      dislikes.value += 1;
    }
  }

  if (type === userReaction.value) {
    userReaction.value = null;
  } else {
    userReaction.value = type;
  }

  const reaction: Reaction = {
    video_id: props.video.video_id,
    type,
  };

  emits("react", reaction);
};

// const emitSeekReaction = (from: number, to: number) => {
//   const Reaction: Reaction = {
//     videoId: props.video.id,
//     type: "seek",
//     timestamp: Date.now(),
//     fromTime: from,
//     toTime: to,
//   };
//   props.onReaction(Reaction);
// };
</script>
