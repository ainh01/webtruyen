
type Route = {
  name: string;
  path: string;
  icon: string;
};

export const routes: Route[] = [
  { name: 'Home', path: '/', icon: 'tabler:home' },
  { name: 'Thể loại', path: '/genres?type=action' , icon: 'tabler:list'},
  { name: 'Truyện Mới', path: '/danh-sach/truyen-moi/' , icon: 'tabler:jewish-star'},
  { name: 'Sắp ra mắt', path: '/danh-sach/sap-ra-mat/' , icon: 'tabler:hourglass-low'},
  { name: 'Đăng nhập', path: '/dang-nhap/' , icon: 'tabler:user-circle'},
  { name: '', path: '/profile/' , icon: 'tabler:user-circle'},
  { name: '', path: '/logout/' , icon: 'tabler:door-exit'},
  
];

type TopRoute = {
  name: string;
  type: string;
  icon: string;
};

export const topRoutes: TopRoute[] = [
  { name: 'Top Comics', type: 'all', icon: 'fontisto:snowflake-6' },
  { name: 'Top Daily', type: 'daily', icon: 'tabler:hexagon-letter-d' },
  { name: 'Top Weekly', type: 'weekly', icon: 'tabler:hexagon-letter-w' },
  { name: 'Top Monthly', type: 'monthly', icon: 'tabler:hexagon-letter-m' },
  {
    name: 'Top Chapter',
    type: 'chapter',
    icon: 'fluent:document-one-page-multiple-20-regular',
  },
  { name: 'Top Follow', type: 'follow', icon: 'ph:users' },
  { name: 'Top Comment', type: 'comment', icon: 'fluent:comment-20-regular' },
];

export const filterValues: { label: string; value: string }[] = [
  { label: 'All', value: 'all' },
  { label: 'Completed', value: 'completed' },
  { label: 'Ongoing', value: 'ongoing' },
  { label: 'Coming Soon', value: 'coming_soon' },
];

type DynamicRoute = {
  path: string;
  apiPath: string;
  title: string;
  icon: string;
};

export const dynamicRoutes: DynamicRoute[] = [
  {
    path: '/the-loai/action',
    apiPath: '',
    title: 'Action',
    icon: '',
  },
  {
    path: '/the-loai/adult',
    apiPath: '',
    title: 'Adult',
    icon: '',
  },
  {
    path: '/the-loai/adventure',
    apiPath: '',
    title: 'Adventure',
    icon: '',
  },
  {
    path: '/the-loai/anime',
    apiPath: '',
    title: 'Anime',
    icon: '',
  },
  {
    path: '/the-loai/chuyen-sinh',
    apiPath: '',
    title: 'Chuyển Sinh',
    icon: '',
  },
  {
    path: '/the-loai/comedy',
    apiPath: '',
    title: 'Comedy',
    icon: '',
  },
  {
    path: '/the-loai/comic',
    apiPath: '',
    title: 'Comic',
    icon: '',
  },
  {
    path: '/the-loai/cooking',
    apiPath: '',
    title: 'Cooking',
    icon: '',
  },
  {
    path: '/the-loai/co-dai',
    apiPath: '',
    title: 'Cổ Đại',
    icon: '',
  },
  {
    path: '/the-loai/doujinshi',
    apiPath: '',
    title: 'Doujinshi',
    icon: '',
  },
  {
    path: '/the-loai/drama',
    apiPath: '',
    title: 'Drama',
    icon: '',
  },
  {
    path: '/the-loai/dam-my',
    apiPath: '',
    title: 'Đam Mỹ',
    icon: '',
  },
  {
    path: '/the-loai/ecchi',
    apiPath: '',
    title: 'Ecchi',
    icon: '',
  },
  {
    path: '/the-loai/fantasy',
    apiPath: '',
    title: 'Fantasy',
    icon: '',
  },
  {
    path: '/the-loai/gender-bender',
    apiPath: '',
    title: 'Gender Bender',
    icon: '',
  },
  {
    path: '/the-loai/harem',
    apiPath: '',
    title: 'Harem',
    icon: '',
  },
  {
    path: '/the-loai/historical',
    apiPath: '',
    title: 'Historical',
    icon: '',
  },
  {
    path: '/the-loai/horror',
    apiPath: '',
    title: 'Horror',
    icon: '',
  },
  {
    path: '/the-loai/josei',
    apiPath: '',
    title: 'Josei',
    icon: '',
  },
  {
    path: '/the-loai/live-action',
    apiPath: '',
    title: 'Live action',
    icon: '',
  },
  {
    path: '/the-loai/manga',
    apiPath: '',
    title: 'Manga',
    icon: '',
  },
  {
    path: '/the-loai/manhua',
    apiPath: '',
    title: 'Manhua',
    icon: '',
  },
  {
    path: '/the-loai/manhwa',
    apiPath: '',
    title: 'Manhwa',
    icon: '',
  },
  {
    path: '/the-loai/martial-arts',
    apiPath: '',
    title: 'Martial Arts',
    icon: '',
  },
  {
    path: '/the-loai/mature',
    apiPath: '',
    title: 'Mature',
    icon: '',
  },
  {
    path: '/the-loai/mecha',
    apiPath: '',
    title: 'Mecha',
    icon: '',
  },
  {
    path: '/the-loai/mystery',
    apiPath: '',
    title: 'Mystery',
    icon: '',
  },
  {
    path: '/the-loai/ngon-tinh',
    apiPath: '',
    title: 'Ngôn Tình',
    icon: '',
  },
  {
    path: '/the-loai/one-shot',
    apiPath: '',
    title: 'One shot',
    icon: '',
  },
  {
    path: '/the-loai/psychological',
    apiPath: '',
    title: 'Psychological',
    icon: '',
  },
  {
    path: '/the-loai/romance',
    apiPath: '',
    title: 'Romance',
    icon: '',
  },
  {
    path: '/the-loai/school-life',
    apiPath: '',
    title: 'School Life',
    icon: '',
  },
  {
    path: '/the-loai/sci-fi',
    apiPath: '',
    title: 'Sci-fi',
    icon: '',
  },
  {
    path: '/the-loai/seinen',
    apiPath: '',
    title: 'Seinen',
    icon: '',
  },
  {
    path: '/the-loai/shoujo',
    apiPath: '',
    title: 'Shoujo',
    icon: '',
  },
  {
    path: '/the-loai/shoujo-ai',
    apiPath: '',
    title: 'Shoujo Ai',
    icon: '',
  },
  {
    path: '/the-loai/shounen',
    apiPath: '',
    title: 'Shounen',
    icon: '',
  },
  {
    path: '/the-loai/shounen-ai',
    apiPath: '',
    title: 'Shounen Ai',
    icon: '',
  },
  {
    path: '/the-loai/slice-of-life',
    apiPath: '',
    title: 'Slice of Life',
    icon: '',
  },
  {
    path: '/the-loai/smut',
    apiPath: '',
    title: 'Smut',
    icon: '',
  },
  {
    path: '/the-loai/soft-yaoi',
    apiPath: '',
    title: 'Soft Yaoi',
    icon: '',
  },
  {
    path: '/the-loai/soft-yuri',
    apiPath: '',
    title: 'Soft Yuri',
    icon: '',
  },
  {
    path: '/the-loai/sports',
    apiPath: '',
    title: 'Sports',
    icon: '',
  },
  {
    path: '/the-loai/supernatural',
    apiPath: '',
    title: 'Supernatural',
    icon: '',
  },
  {
    path: '/the-loai/tap-chi-truyen-tranh',
    apiPath: '',
    title: 'Tạp chí truyện tranh',
    icon: '',
  },
  {
    path: '/the-loai/thieu-nhi',
    apiPath: '',
    title: 'Thiếu Nhi',
    icon: '',
  },
  {
    path: '/the-loai/tragedy',
    apiPath: '',
    title: 'Tragedy',
    icon: '',
  },
  {
    path: '/the-loai/trinh-tham',
    apiPath: '',
    title: 'Trinh Thám',
    icon: '',
  },
  {
    path: '/the-loai/truyen-scan',
    apiPath: '',
    title: 'Truyện scan',
    icon: '',
  },
  {
    path: '/the-loai/truyen-mau',
    apiPath: '',
    title: 'Truyện Màu',
    icon: '',
  },
  {
    path: '/the-loai/viet-nam',
    apiPath: '',
    title: 'Việt Nam',
    icon: '',
  },
  {
    path: '/the-loai/webtoon',
    apiPath: '',
    title: 'Webtoon',
    icon: '',
  },
  {
    path: '/the-loai/xuyen-khong',
    apiPath: '',
    title: 'Xuyên Không',
    icon: '',
  },
  {
    path: '/the-loai/16',
    apiPath: '',
    title: '16+',
    icon: '',
  }
];

export const meta = (data?: {
  title?: string;
  description?: string;
  image?: string;
}) => {
  const title = data?.title;
  const description = data?.description;
  return {
    title: title || 'NComics | Free comics and manga reader online',
    ogTitle: title || 'NComics | Free comics and manga reader online',
    description:
      description ||
      'Read hottest Japanese manga & Chinese comic & anime & Webtoon released on NComics. Thousands of popular web manga and comics for free! Romance, thriller, fantasy, comedy and more genres for you to explore.',
    ogDescription:
      description ||
      'Read hottest Japanese manga & Chinese comic & anime & Webtoon released on NComics. Thousands of popular web manga and comics for free! Romance, thriller, fantasy, comedy and more genres for you to explore.',
    ogImage: data?.image || '@/assets/img/logo.svg',
  };
};
