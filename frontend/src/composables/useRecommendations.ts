// src/composables/useRecommendations.ts
import { ref } from "vue";
import type { Reaction, Video } from "../types";
import axios from "axios";
import { v4 as uuidv4 } from 'uuid';

const apiBaseUrl = "http://51.250.29.17:8000";

export function useRecommendations() {
  // Генерация уникального ID, чтобы рекомендации для пользователей не перемешивались
  // В проде будут использоваться авторизационные данные
  const clientId = uuidv4();
  const recommendedVideos = ref<Video[]>([]);

  const fetchInitialVideos = async () => {
    try {
      const response = await axios.get(`${apiBaseUrl}/api/top-videos`, {
        params: {
          client_id: clientId,
        },
      });
      recommendedVideos.value = response.data.data;
    } catch (err: any) {
      return err.response?.data?.error || "An error occurred";
    }
  };

  const fetchRelatedVideos = async (videoId: string) => {
    try {
      const response = await axios.get(`${apiBaseUrl}/api/related-videos`, {
        params: {
          video_id: videoId,
          client_id: clientId,
        },
      });
      recommendedVideos.value = response.data.data;
    } catch (err: any) {
      return err.response?.data?.error || "An error occurred";
    }
  };

  const fetchRecommendedVideos = async (reaction: Reaction) => {
    // 0 - дизлайк
    // 1 - игнор
    // 2 - лайк

    try {
      let reactionCode = 1;

      if (reaction.type === "like") {
        reactionCode = 2;
      } else if (reaction.type === "dislike") {
        reactionCode = 0;
      } else {
        reactionCode = 1;
      }

      const response = await axios.get(`${apiBaseUrl}/api/recommended-videos`, {
        params: {
          video_id: reaction.video_id,
          reaction: reactionCode,
          client_id: clientId,
        },
      });
      recommendedVideos.value = response.data.data;
    } catch (err: any) {
      return err.response?.data?.error || "An error occurred";
    }
  };

  return {
    recommendedVideos,
    fetchInitialVideos,
    fetchRecommendedVideos,
    fetchRelatedVideos,
  };
}
