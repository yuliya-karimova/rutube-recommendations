// src/composables/useRecommendations.ts
import { ref } from "vue";
import type { Reaction, Video } from "../types";

const fakeVideo = [
  {
    video_id: "973f24c0-15b2-434f-8740-4e2726f79c30",
    title:
      "ЗИМНЯЯ, ТЕПЛАЯ ШЛЯПА крючком. Как связать поля шляпы. Видео для начинающих",
    description:
      "Шляпа связана из пряжи NAKO Sport Wool в 100гр.-120м., крючок 5мм., расход пряжи на шляпу 200гр.  Ссылка на шапочку",
    category_id: "Полезное",
    v_pub_datetime: "2024-06-15T19:58:03.000Z",
    v_total_comments: 5,
    v_year_views: 120,
    v_likes: 43,
    v_dislikes: 3,
    v_duration: 379,
    author_id: "9afa94aa-c2a6-43fc-a0d1-175eaf7fa194",
  },
  {
    video_id: "sadav-15b2-saf4234-8740-4e2726f79c30",
    title: "Рафтинг Марафон 2024",
    description:
      "Рафтинг Марафон 2024 ВК:https://vk.com/dmitriy.kolos YouTube:https://www.youtube.com/@Krasnoyarsk1313/featured",
    category_id: "Путешествия",
    v_pub_datetime: "2023-08-15T19:58:03.000Z",
    v_total_comments: 242,
    v_year_views: 35353,
    v_likes: 423,
    v_dislikes: 0,
    v_duration: 523,
    author_id: "34324-c2a6-dsad-a0d1-175eaf7fa194",
  },
  {
    video_id: "324-15b2-saf4234-8740-4e2726f79c30",
    title: "СПАСТИСЬ ОТ АКУЛЫ НА КОРАБЛЕ - SHARK SIEGE SURVIVAL [Первый взгляд]",
    description:
      "Прохождение игры SHARK SIEGE SURVIVAL. Меня зовут Михаил, рад видеть тебя на нашем с тобой канале, я люблю играть в игры и выкладываю по ним прохождения :)",
    category_id: "Видеоигры",
    v_pub_datetime: "2024-08-15T19:58:03.000Z",
    v_total_comments: 1,
    v_year_views: 12,
    v_likes: 4,
    v_dislikes: 12,
    v_duration: 4243,
    author_id: "4324234-c2a6-dsad-a0d1-175eaf7fa194",
  },
];

const fakeVideos = [
  ...fakeVideo,
  ...fakeVideo,
  ...fakeVideo,
  fakeVideo[0],
];

export function useRecommendations() {
  const recommendedVideos = ref<Video[]>([]);

  const fetchInitialVideos = async (): Promise<Video[]> => {
    console.log("🚀 ~ fetchInitialVideos ~ fetchInitialVideos:")
    return new Promise((resolve) => {
      setTimeout(() => {
        recommendedVideos.value = fakeVideos;
        resolve(fakeVideos);
      }, 300);
    });
  };

  const fetchRecommendedVideos = async (
    reaction: Reaction
  ): Promise<Video[]> => {
    console.log("🚀 ~ useRecommendations ~ reaction:", reaction)
    return new Promise((resolve) => {
      setTimeout(() => {
        recommendedVideos.value = fakeVideos;
        resolve(fakeVideos);
      }, 300);
    });
  };

  const fetchRelatedVideos = async (videoId: string): Promise<Video[]> => {
    console.log("🚀 ~ fetchRelatedVideos ~ videoId:", videoId)
    return new Promise((resolve) => {
      setTimeout(() => {
        recommendedVideos.value = fakeVideos;
        resolve(fakeVideos);
      }, 300);
    });
  };

  return {
    recommendedVideos,
    fetchInitialVideos,
    fetchRecommendedVideos,
    fetchRelatedVideos,
  };
}
