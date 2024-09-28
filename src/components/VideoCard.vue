<template>
  <div
    class="bg-gray-800 text-white p-4 rounded-xl flex flex-col gap-1 text-xs"
  >
    <div class="line-clamp-2 font-bold text-base mb-1">{{ video.title }}</div>
    <div class="text-gray-500 line-clamp-2">
      {{ video.description }}
    </div>
    <div>Категория: {{ video.category_id }}</div>
    <div>Опубликовано: {{ formattedDate }}</div>
    <div>Просмотры: {{ video.v_year_views }}</div>
    <div>Комментарии: {{ video.v_total_comments }}</div>
  </div>
</template>

<script lang="ts" setup>
import { computed } from "vue";
import type { Video } from "../types";
import dayjs from "dayjs";

const props = defineProps<{
  video: Video;
}>();

const formattedDate = computed(() => {
  return props.video.v_pub_datetime
    ? dayjs(props.video.v_pub_datetime).format("YYYY-MM-DD")
    : "";
});
</script>
