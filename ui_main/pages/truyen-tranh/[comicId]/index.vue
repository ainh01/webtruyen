<script lang="ts" setup>
import {  type Comment, type UserInfo } from '@/types';
import { meta } from '@/utils/data';
import { getUserInfoFromLocalStorage } from '@/utils/localDb';
import axios from 'axios';


type ChapterDetail = {
  id: number;
  chapter_name: string;
  chapter_api_data: string;
};

type Tab = 'chapters' | 'comments';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

const route = useRoute();
const comicId = route.params.comicId as string;
const CHAPTER_PER_PAGE = 50;

const chaptersSection = ref<ChapterDetail[]>([]);
const currentTab = ref<Tab>('chapters');
const comments = ref<Comment[]>([]);
const description = ref<any>(null);

const commentPage = ref<number>(1);
const currentChapterPage = ref<number>(0);
const isEnd = ref<boolean>(false);

const isFetching = ref<boolean>(false);
const isTooLongDescription = ref<boolean>(false);
const showFullDescription = ref<boolean>(false);

const showChapterSelection = ref<boolean>(false);
const currentDownloadChapterPage = ref<number>(0);
const chaptersDownloadSection = ref<ChapterDetail[]>([]);
const showDownloadModal = ref<boolean>(false);
const downloadChapters = ref<string[]>([]);

const userInfo = ref<UserInfo | null>(getUserInfoFromLocalStorage() as UserInfo | null);

const isFavorite = ref<boolean>(false); // Initial favorite status

const latestChapter = ref<string>('');

// Fetch comic detail
const [comicDetail] = await Promise.all([useFetchData(`/truyen-tranh/${comicId}`)]);
const comic = comicDetail.data.item;

// Hàm lấy chapter mới nhất dựa vào comicId
const fetchLatestChapter = (comicId: string, historyComics: any[]): string | null => {
  // Lọc danh sách theo comicId
  const filteredComics = historyComics.filter((item) => item.id_comic === comicId);

  if (filteredComics.length === 0) {
    return null; // Nếu không có dữ liệu, trả về null
  }

  // Tìm chapter mới nhất bằng reduce
  const latestComic = filteredComics.reduce((latest, current) => {
    return new Date(current.updated_at) > new Date(latest.updated_at) ? current : latest;
  });

  return latestComic.chapter_name; // Trả về chapter_name của chương mới nhất
};

// Hàm fetch danh sách history comics và xác định chương mới nhất
const fetchHistoryComics = async () => {
  if (userInfo.value && userInfo.value.email) {
    try {
      // Gọi API lấy danh sách history comics
      const historyComicsResponse = await useFetchData_MyAPI('/get_history_comics', {
        email: userInfo.value.email,
      });

      if (historyComicsResponse && historyComicsResponse.data) {
        const historyComics = historyComicsResponse.data;

        // Lấy chapter mới nhất cho comicId hiện tại
        const latestChapterName = fetchLatestChapter(comicId, historyComics);

        if (latestChapterName) {
          latestChapter.value = latestChapterName; // Gán giá trị vào ref latestChapter
        }
      }
    } catch (error) {
      console.error('Error fetching favorite status:', error);
    }
  }
};

await fetchHistoryComics();

// Toggle favorite status
const toggleFavorite = async () => {
  if (!userInfo.value) {
    alert('Bạn cần đăng nhập để sử dụng chức năng này!');
    return;
  }

  try {
    // Send a request to toggle favorite status
    const response = await axios.post(`${API_BASE_URL}/set_favorite_client`, {
      email: userInfo.value.email,
      id_comic: comicId,
      status: !isFavorite.value, // Toggle the status
    });

    if (response.data.message === 'Data set successfully') {
      // Update the favorite status after successful request
      isFavorite.value = !isFavorite.value;
    } else {
      alert('Không thể lưu trạng thái yêu thích. Vui lòng thử lại.');
    }
  } catch (error) {
    console.error('Error toggling favorite status:', error);
    alert('Đã xảy ra lỗi. Vui lòng thử lại sau.');
  }
};

// Function to check favorite status
const fetchFavoriteStatus = async () => {
  if (userInfo.value && userInfo.value.email) {
    try {
      const favoriteStatus = await useFetchData_MyAPI('/get_favorite_client', {
        email: userInfo.value.email,
        id_comic: comicId,
      });

      if (favoriteStatus) {
        isFavorite.value = favoriteStatus.status;
      }
    } catch (error) {
      console.error('Error fetching favorite status:', error);
    }
  }
};

// // Calling fetchFavoriteStatus to initialize the favorite status
await fetchFavoriteStatus();

// Ensure comic.chapters is an array
const chapters = Array.isArray(comic.chapters) ? comic.chapters : [];
const serverData = Array.isArray(chapters[0].server_data) ? chapters[0].server_data : [];
const total_chapter = serverData.length; 

// console.log(chapters[0].server_data);
// console.log(total_chapter);

const totalChapterPage = !isNaN(Number(total_chapter))
  ? Math.ceil(Number(total_chapter) / CHAPTER_PER_PAGE)
  : 0;

// console.log(totalChapterPage);


const getChapter = (start: number, end: number) => {
  const limit = CHAPTER_PER_PAGE * 6;
  const chapters = serverData
    .filter(( chapter : any, idx: number) => {
      if(idx >= start && idx <= end){
        return true
      }
      return false
    });
  return chapters;
};


chaptersSection.value = getChapter(0, CHAPTER_PER_PAGE);
chaptersDownloadSection.value = getChapter(0, CHAPTER_PER_PAGE);

const onChangeChapterGroup = (idx: number) => {
  currentChapterPage.value = idx;
  chaptersSection.value = getChapter(
    idx === 0 ? 0 : idx * CHAPTER_PER_PAGE + 1,
    (idx + 1) * CHAPTER_PER_PAGE
  );
};

// Hàm để xử lý khi chọn hoặc bỏ chọn chapter
const onAddDownloadChapter = (chapterName: string): void => {
  if (!chapterName || typeof chapterName !== "string") {
    console.error("Chapter name không hợp lệ:", chapterName);
    return;
  }

  const index = downloadChapters.value.indexOf(chapterName);

  if (index === -1) {
    // Thêm chapter vào mảng downloadChapters
    downloadChapters.value.push(chapterName);
  } else {
    // Xóa chapter khỏi mảng downloadChapters nếu đã có trong đó
    downloadChapters.value.splice(index, 1);
  }

  console.log("Danh sách chương đã chọn:", downloadChapters);
};

// Hàm thay đổi nhóm chương để tải về
const onChangeChapterDownloadGroup = (idx: number) => {
  currentDownloadChapterPage.value = idx;
  chaptersDownloadSection.value = getChapter(
    idx === 0 ? 0 : idx * CHAPTER_PER_PAGE + 1,
    (idx + 1) * CHAPTER_PER_PAGE
  );
};

// Hàm gửi yêu cầu tải xuống qua API
const handleDownloadChapters = async () => {
  if (!userInfo.value) {
    alert('Bạn cần đăng nhập để sử dụng chức năng này!');
    return;
  }

  if (!downloadChapters.value.length) {
    alert('Vui lòng chọn ít nhất một chương để tải xuống!');
    return;
  }

  console.log('chapter_ids:', downloadChapters.value);

  try {
    isFetching.value = true; // Hiển thị trạng thái đang tải
    alert('Đang xử lý yêu cầu, vui lòng chờ...');

    // Chuyển các chapter thành mảng đúng định dạng (không có dấu ngoặc kép thừa)
    const requestData = downloadChapters.value.map(chapter => `${chapter}`);

    // Gửi yêu cầu POST với query string comic_id và dữ liệu là mảng các chapter_ids
    const response = await axios.post(
      `${API_BASE_URL}/download_comic?comic_id=${comicId}`,
      requestData,
      {
        headers: {
          'accept': 'application/json',
          'Content-Type': 'application/json',
        },
        responseType: 'blob', // Đảm bảo API trả về file PDF
      }
    );

    // Tạo liên kết tải file
    const blob = new Blob([response.data], { type: 'application/pdf' });
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `${comicId}.pdf`;
    link.click();

    // Dọn dẹp liên kết blob sau khi tải xong
    window.URL.revokeObjectURL(url);
    isFetching.value = false;
    alert('Tải xuống thành công!');
    showDownloadModal.value = false; // Đóng modal sau khi tải xuống

  } catch (error) {
    console.error('Lỗi khi tải xuống:', error);
    isFetching.value = false;
    alert('Đã xảy ra lỗi khi tải xuống. Vui lòng thử lại sau.');
  }
};


const addHistoryComic = (chapter_name : string) => {
  if (!userInfo.value) {
    console.error("User info is missing");
    return;
  }

  const payload = {
    email: userInfo.value.email,
    id_comic: comicId,
    chapter_name,
  };

  console.log("Payload being sent:", payload);

  axios
    .post(`${API_BASE_URL}/set_history_comics`, payload)
    .then((response) => {
      console.log("Response:", response.data);
    })
    .catch((error) => {
      console.error("Error:", error.response?.data || error.message);
    });
};


onMounted(() => {
  if (description.value) {
    const { clientHeight, scrollHeight } = description.value;
    isTooLongDescription.value = clientHeight < scrollHeight;
  }
});

watch(showDownloadModal, (status) => {
  document.body.style.overflow = status ? 'hidden' : 'auto';
});

useSeoMeta(
  meta({
    title: comic.name + ' | STORIES',
    description: comic.content,
    image: comic.thumb_url,
  })
);
useServerSeoMeta(
  meta({
    title: comic.name + ' | STORIES',
    description: comic.content,
    image: comic.thumb_url,
  })
);

const baseUrl = 'https://otruyenapi.com/uploads/comics/';
const imageFile = ref(comic.thumb_url);

const imageSrc = computed(() => `${baseUrl}${imageFile.value}`);

</script>


<template>
  <div class="relative pt-12 px-4 min-h-screen">
    <div
      class="absolute top-0 inset-x-0 h-80 bg-gradient-to-b from-slate-100 -z-10"
    />
    <div
      class="max-w-5xl mx-auto border-4 border-transparent p-0 rounded-xl sm:grid sm:grid-cols-4 gap-6 md:p-4 md:border-white"
    >
      <div
        class="aspect-[2/3] w-56 mx-auto sm:w-full rounded-lg border-2 overflow-hidden border-[#2dce89] relative sm:col-span-1"
      >
        <img
          class="w-full h-full object-cover"
          :src="imageSrc"
          :alt="comic.name"
          draggable="false"
        />
        <div
          class="flex gap-1 absolute font-bold top-0 inset-x-0 z-10 text-xs text-white"
        >
          <span
            v-if="comic.status === 'Finished'"
            class="bg-sky-500 py-0.5 px-2 rounded-b-sm first:rounded-bl-none"
          >
            End
          </span>
        </div>
      </div>
      <div class="sm:col-span-3">
        <div class="flex justify-between items-center">
          <h4 class="text-3xl font-extrabold mt-5 sm:mt-0">{{ comic.name }}</h4>

          <div class="heart-container" title="Like">
            <input
              type="checkbox"
              class="checkbox"
              id="Give-It-An-Id"
              :checked="isFavorite"
              @click="toggleFavorite"
            />
            
            <div class="svg-container">
              <svg viewBox="0 0 24 24" class="svg-outline" xmlns="http://www.w3.org/2000/svg">
                <path
                  d="M17.5,1.917a6.4,6.4,0,0,0-5.5,3.3,6.4,6.4,0,0,0-5.5-3.3A6.8,6.8,0,0,0,0,8.967c0,4.547,4.786,9.513,8.8,12.88a4.974,4.974,0,0,0,6.4,0C19.214,18.48,24,13.514,24,8.967A6.8,6.8,0,0,0,17.5,1.917Zm-3.585,18.4a2.973,2.973,0,0,1-3.83,0C4.947,16.006,2,11.87,2,8.967a4.8,4.8,0,0,1,4.5-5.05A4.8,4.8,0,0,1,11,8.967a1,1,0,0,0,2,0,4.8,4.8,0,0,1,4.5-5.05A4.8,4.8,0,0,1,22,8.967C22,11.87,19.053,16.006,13.915,20.313Z"
                ></path>
              </svg>
              <svg viewBox="0 0 24 24" class="svg-filled" xmlns="http://www.w3.org/2000/svg">
                <path
                  d="M17.5,1.917a6.4,6.4,0,0,0-5.5,3.3,6.4,6.4,0,0,0-5.5-3.3A6.8,6.8,0,0,0,0,8.967c0,4.547,4.786,9.513,8.8,12.88a4.974,4.974,0,0,0,6.4,0C19.214,18.48,24,13.514,24,8.967A6.8,6.8,0,0,0,17.5,1.917Z"
                ></path>
              </svg>

              <svg class="svg-celebrate" width="100" height="100" xmlns="http://www.w3.org/2000/svg">
                <polygon points="10,10 20,20"></polygon>
                <polygon points="10,50 20,50"></polygon>
                <polygon points="20,80 30,70"></polygon>
                <polygon points="90,10 80,20"></polygon>
                <polygon points="90,50 80,50"></polygon>
                <polygon points="80,80 70,70"></polygon>
              </svg>
            </div>
          </div>

        </div>
        <div class="font-bold text-sm flex flex-wrap items-center gap-2 my-1">
          <NuxtLink
            v-for="genre in comic.category"
            :to="`/the-loai/${genre.slug}?page=1`"
            class="px-2 py-0.5 rounded bg-transparent border-2 border-slate-300 duration-100 hover:bg-slate-300"
          >
            {{ genre.name }}
          </NuxtLink>
        </div>
        <div class="font-semibold flex items-center gap-2 my-1">
          Tác giả:
          <template v-if="Array.isArray(comic.author)">
            <div v-for="(author, idx) in comic.author" :key="author">
              <NuxtLink
                :to="`/search?keyword=${author.replace(/\s+/g, '+')}`"
                class="text-fuchsia-500"
              >
                {{ author }}
              </NuxtLink>
              <span class="select-none" v-if="idx < comic.author.length - 1">
                -
              </span>
            </div>
          </template>
          
          <template v-else>
            <NuxtLink
                :to="`/search?keyword=${(comic.author || '').replace(/\s+/g, '+')}`"
                class="text-fuchsia-500"
              >
                {{ comic.author }}
            </NuxtLink>

          </template>
        </div>
        <div class="mt-2" v-if="comic.content">
          <p
            :class="showFullDescription ? 'line-clamp-none' : 'line-clamp-5'"
            ref="description"
          >
            <span v-html="comic.content"></span>
          </p>
          <button
            v-if="isTooLongDescription"
            class="font-semibold hover:underline"
            @click="showFullDescription = !showFullDescription"
          >
            {{ showFullDescription ? 'Show less' : 'Show more' }}
          </button>
        </div>
        <div
          class="flex flex-col sm:flex-row items-center gap-3 mt-5 font-bold"
        >
          <button
          @click="
              () => {
                if (!comic.chapters || !comic.chapters.length) return;
                navigateTo(`/truyen-tranh/${comic.slug}/1`);
              }
            "
            :class="`btn-more ${
              comic.chapters && comic.chapters.length
                ? 'border-[#2dce89] bg-[#2dce89]'
                : 'border-gray-500 bg-gray-500'
            }`"
            :disabled="!comic.chapters || !comic.chapters.length"

          >
            <div class="svg-wrapper-1">
              <div class="svg-wrapper">
                <svg  xmlns="http://www.w3.org/2000/svg"  width="24"  height="24"  viewBox="0 0 24 24"  fill="none"  stroke="currentColor"  stroke-width="2"  stroke-linecap="round"  stroke-linejoin="round"  class="icon icon-tabler icons-tabler-outline icon-tabler-book"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><path d="M3 19a9 9 0 0 1 9 0a9 9 0 0 1 9 0" /><path d="M3 6a9 9 0 0 1 9 0a9 9 0 0 1 9 0" /><path d="M3 6l0 13" /><path d="M12 6l0 13" /><path d="M21 6l0 13" /></svg>
              </div>
            </div>
            <span>Đọc</span>
          </button>

          <button
            @click="showDownloadModal = true"
            :class="`btn-more ${
              comic.chapters && comic.chapters.length
                ? 'border-[#2dce89] bg-[#2dce89]'
                : 'border-gray-500 bg-gray-500'
            }`"
            :disabled="!comic.chapters || !comic.chapters.length"
          >
            <div class="svg-wrapper-1">
              <div class="svg-wrapper">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  width="24"
                  height="24"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="2"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  class="icon icon-tabler icon-tabler-download"
                >
                  <path stroke="none" d="M0 0h24v24H0z" fill="none" />
                  <path d="M4 17v2a2 2 0 0 0 2 2h12a2 2 0 0 0 2 -2v-2" />
                  <path d="M7 11l5 5l5 -5" />
                  <path d="M12 4l0 12" />
                </svg>
              </div>
            </div>
            <span>Download</span>
          </button>

        </div>
      </div>
    </div>
    <div class="max-w-5xl mx-auto mt-5">
      <div
        class="flex items-center gap-6 font-bold text-lg sm:text-xl border-b-2 py-1"
      >
        <button
          :class="`flex items-center gap-1 ${
            currentTab === 'chapters' ? 'text-[#2dce89]' : ''
          }`"
          @click="currentTab = 'chapters'"
        >
          <Icon name="bytesize:book" size="20" />
          Chapters
        </button>
      </div>
      <div v-show="currentTab === 'chapters'">
        <h4
          class="mt-6 text-center text-2xl font-bold text-gray-700 select-none"
          v-if="!comic.chapters || !comic.chapters.length"
        >
          No Chapter
        </h4>
        <div
          v-else
          class="flex items-center gap-3 my-5 text-gray-800 font-semibold text-sm flex-wrap"
        >
          <button
            v-for="(_, idx) in new Array(totalChapterPage)"
            :class="`px-2 py-0.5 rounded-full ${
              idx === currentChapterPage
                ? 'bg-slate-100 text-[#2dce89]'
                : 'bg-gray-100'
            }`"
            @click="onChangeChapterGroup(idx)"
          >
            <template v-if="idx + 1 < totalChapterPage">
              {{
                `${idx === 0 ? 0 : idx * CHAPTER_PER_PAGE + 1} - ${
                  (idx + 1) * CHAPTER_PER_PAGE
                }`
              }}
            </template>
            <template v-else>
              {{
                `${
                  totalChapterPage === 1 ? 0 : idx * CHAPTER_PER_PAGE + 1
                } - ${total_chapter}`
              }}
            </template>
          </button>
        </div>
        <ul class="grid grid-cols-2 md:grid-cols-4 gap-4">
          <NuxtLink
            v-for="chapter in chaptersSection"
            :key="chapter.chapter_name"
            class="border rounded px-3 py-2 truncate hover:bg-slate-50 duration-100"
            :class="{'bg-yellow-100 border-yellow-400': chapter.chapter_name === latestChapter}"
            :to="`/truyen-tranh/${comicId}/${chapter.chapter_name}`"
            @click="addHistoryComic(chapter.chapter_name)"
          >
            <abbr :title="chapter.chapter_name" class="no-underline">
              Chap {{ chapter.chapter_name }}
            </abbr>
          </NuxtLink>
        </ul>
      </div>
      
    </div>
  </div>
  <!-- Download -->
  <div
    :class="`fixed z-50 inset-0 bg-[rgba(0,0,0,0.8)] flex flex-col items-center justify-center duration-200 ${
      showDownloadModal
        ? 'opacity-1 pointer-events-auto'
        : 'opacity-0 pointer-events-none'
    }`"
  >
    <div class="bg-white rounded-lg py-4 px-6 w-[90vw] max-w-3xl">
      <div class="flex flex-col sm:flex-row items-center gap-2.5 sm:gap-5">
        <h3 class="text-2xl font-semibold">Select chapters</h3>
        <div
          class="border rounded px-3 py-1 relative cursor-pointer"
          @click="showChapterSelection = !showChapterSelection"
        >
          Chapters
          <Icon name="icon-park-outline:down" size="24" class="ml-2" />
          <ul
            class="absolute top-10 w-40 right-1/2 translate-x-1/2 border rounded bg-white max-h-60 overflow-auto"
            v-show="showChapterSelection"
          >
            <li
              v-for="(_, idx) in new Array(totalChapterPage)"
              :class="`px-2 py-1 border-b last:border-b-0 ${
                idx === currentDownloadChapterPage
                  ? 'text-[#2dce89] font-medium'
                  : ''
              }`"
              @click="onChangeChapterDownloadGroup(idx)"
            >
              <template v-if="idx + 1 < totalChapterPage">
                {{
                  `${idx === 0 ? 0 : idx * CHAPTER_PER_PAGE + 1} - ${
                    (idx + 1) * CHAPTER_PER_PAGE
                  }`
                }}
              </template>
              <template v-else>
                {{
                  `${
                    totalChapterPage === 1 ? 0 : idx * CHAPTER_PER_PAGE + 1
                  } - ${total_chapter}`
                }}
              </template>
            </li>
          </ul>
        </div>
      </div>
      <ul
        class="grid sm:grid-cols-2 md:grid-cols-4 lg:grid-cols-5 gap-3 max-h-[45vh] overflow-auto my-3 py-1 pr-1 select-none"
      >
        <li
          v-for="chapter in chaptersDownloadSection"
          :key="chapter.id"
          :class="`border rounded px-2 py-1 cursor-pointer duration-100 truncate ${
            downloadChapters.includes(chapter.chapter_name)
              ? 'border-[#2dce89] bg-[#2dce89] text-white'
              : ''
          }`"
          @click="onAddDownloadChapter(chapter.chapter_name)"
        >
          {{ chapter.chapter_name }}
        </li>

      </ul>
      <div class="flex items-center justify-end gap-5 font-medium">
        <button class="text-rose-500" @click="showDownloadModal = false">
          Cancel
        </button>
        <button
          :class="`text-white px-2.5 py-1.5 rounded flex items-center gap-1.5 ${
            downloadChapters.length
              ? 'border-[#2dce89] bg-[#2dce89]'
              : 'border-gray-500 bg-gray-500'
          }`"
          @click="handleDownloadChapters"
          :disabled="!downloadChapters.length|| isFetching"
        >
          <template v-if="isFetching">
            <svg class="animate-spin h-5 w-5 mr-2" viewBox="0 0 24 24">
              <circle
                class="opacity-25"
                cx="12"
                cy="12"
                r="10"
                stroke="currentColor"
                stroke-width="4"
                fill="none"
              ></circle>
              <path
                class="opacity-75"
                fill="currentColor"
                d="M4 12a8 8 0 018-8v8H4z"
              ></path>
            </svg>
            Processing...
          </template>
          <template v-else>
            Download
          </template>
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
@media only screen and (min-width: 320px) and (max-width: 576px) {
  .responsive-devices {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}
@media only screen and (min-width: 576px) and (max-width: 768px) {
  .responsive-devices {
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 0.5rem;
  }
  .title {
    font-size: 1.5rem;
    line-height: 2rem;
  }
}

/* From Uiverse.io by catraco */ 
.heart-container {
  --heart-color: rgb(255, 91, 137);
  position: relative;
  width: 35px;
  height: 35px;
  transition: .3s;
}

.heart-container .checkbox {
  position: absolute;
  width: 100%;
  height: 100%;
  opacity: 0;
  z-index: 20;
  cursor: pointer;
}

.heart-container .svg-container {
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}

.heart-container .svg-outline,
        .heart-container .svg-filled {
  fill: var(--heart-color);
  position: absolute;
}

.heart-container .svg-filled {
  animation: keyframes-svg-filled 1s;
  display: none;
}

.heart-container .svg-celebrate {
  position: absolute;
  animation: keyframes-svg-celebrate .5s;
  animation-fill-mode: forwards;
  display: none;
  stroke: var(--heart-color);
  fill: var(--heart-color);
  stroke-width: 2px;
}

.heart-container .checkbox:checked~.svg-container .svg-filled {
  display: block
}

.heart-container .checkbox:checked~.svg-container .svg-celebrate {
  display: block
}

@keyframes keyframes-svg-filled {
  0% {
    transform: scale(0);
  }

  25% {
    transform: scale(1.2);
  }

  50% {
    transform: scale(1);
    filter: brightness(1.5);
  }
}

@keyframes keyframes-svg-celebrate {
  0% {
    transform: scale(0);
  }

  50% {
    opacity: 1;
    filter: brightness(1.5);
  }

  100% {
    transform: scale(1.4);
    opacity: 0;
    display: none;
  }
}
</style>
