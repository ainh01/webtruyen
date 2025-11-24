
export type ComicDetail = {
  _id: string;
  name: string;
  slug: string;
  origin_name: string | string[];
  content: string;
  status: string;
  thumb_url: string;
  sub_docquyen: boolean;
  author: string[];
  category: {
    id: string;
    name: string;
    slug: string;
  }[];
  chapters: {
    server_name: string;
    server_data: {
      filename: string;
      chapter_name: string;
      chapter_title: string;
      chapter_api_data: string;
    }[];
  }[];
  updatedAt: string;
};

export type Comic = {
  _id: string;
  name: string;
  slug: string;
  origin_name: string | string[];
  status: string;
  thumb_url: string;
  sub_docquyen: boolean;
  category: {
    id: string;
    name: string;
    slug: string;
  }[];
  updatedAt: string;
  chaptersLatest: {
    filename: string;
    chapter_name: string;
    chapter_title: string;
    chapter_api_data: string;
  }[];
  chapters?: Array<{
    id: string;
    title: string;
  }>;
  description?: string;
  thumbnail: string;
  title: string;
  id: string;
}

export type Reply = {
  avatar: string;
  content: string;
  created_at: string;
  username: string;
  stickers: string[];
  vote_count: number;
  mention_user: string;
};

export type Comment = {
  avatar: string;
  content: string;
  created_at: string;
  username: string;
  stickers: string[];
  vote_count: number;
  replies: Reply[];
};

export type ComicComments = {
  total_pages: number;
  total_comments: number;
  current_page: number;
  comments: Comment[];
};

export type Genre = {
  name: string;
  id: string;
  description?: string;
};


export type Genres = {
  _id: string;
  name: string;
  slug: string;
  origin_name: string[];
  status: "ongoing" | "completed" | "coming_soon";
  thumb_url: string;
  sub_docquyen: boolean;
  category: {
      id: string;
      name: string;
      slug: string;
  }[];
  updatedAt: string;
  chaptersLatest: {
      filename: string;
      chapter_name: string;
      chapter_title: string;
      chapter_api_data: string;
  }[];
};

export type UserInfo = {
  username: string;
  email: string;
};

export interface ComicResponse {
  items: Comic[];
  total?: number;
  current_page?: number;
}

