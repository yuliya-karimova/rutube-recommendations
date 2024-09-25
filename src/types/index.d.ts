// src/types/index.d.ts

export interface Video {
    id: string
    title: string
    description: string
    url: string
    thumbnail: string
  }
  
  export interface Interaction {
    videoId: string
    type: 'play' | 'pause' | 'ended'
    timestamp: number
  }