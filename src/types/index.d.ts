export interface Video {
  video_id: string;
  title: string;
  description: string;
  category_id: string;
  v_pub_datetime: string;
  v_total_comments: number;
  v_year_views: number;
  v_likes: number;
  v_dislikes: number;
  v_duration: number;
  author_id: string;
}

export type ReactionType = 'like' | 'dislike'

export interface Reaction {
  video_id: string
  type: ReactionType
}
