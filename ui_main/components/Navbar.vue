<script lang="ts" setup>
import { routes, dynamicRoutes } from '@/utils/data';
import { saveUserInfoToLocalStorage, getUserInfoFromLocalStorage, clearUserInfoFromLocalStorage } from '@/utils/localDb';
import axios from 'axios';


const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;
const device = ref<'mobile' | 'laptop'>('mobile');
const searchValue = ref<string>('');
let suggestComics = ref<any>([]);
const searchInput = ref<any>(null);
const showSuggest = ref<boolean>(false);
const openSidebar = ref<boolean>(false);

const token = ref<string | null>(null);
const userInfo = ref<any>(getUserInfoFromLocalStorage());
const isLoggedIn = ref<boolean>(false);

// Ensure `localStorage` is only accessed on the client-side
onMounted(async () => {
  try {
    if (typeof window !== 'undefined' && window.localStorage) {
      token.value = localStorage.getItem("token");
      
      if (token.value) {
        const response = await axios.get(`${API_BASE_URL}/user/`, {
          headers: {
            Authorization: `Bearer ${token.value}`,
          },
        });

        if (response && response.data) {
          userInfo.value = response.data;
          saveUserInfoToLocalStorage(response.data, 10000);
          isLoggedIn.value = true;  // Đánh dấu đã đăng nhập
          console.log(response.data);
        } else {
          // Nếu không có response data (không có tài khoản đăng nhập)
          isLoggedIn.value = false;
          console.error("Không có thông tin người dùng trong phản hồi.");
        }
      } else {
        // Trường hợp không có token trong localStorage
        isLoggedIn.value = false;
        console.error("Không có token, không thể lấy thông tin người dùng.");
      }
    }
  } catch (error) {
    // Kiểm tra lỗi 401 (Unauthorized)
    if (axios.isAxiosError(error) && error.response && error.response.status === 401) {
      localStorage.removeItem("token");  // Xóa token khi không hợp lệ
      isLoggedIn.value = false;
      console.error("Token không hợp lệ hoặc đã hết hạn. Vui lòng đăng nhập lại.");
      // Chuyển hướng đến trang đăng nhập (nếu có)
      // router.push("/login");  // Nếu bạn đang sử dụng Vue Router
    } else {
      // Xử lý các lỗi khác
      isLoggedIn.value = false;
      console.error("Lỗi khi lấy thông tin người dùng:", error);
    }
  }
});


const handleLogout = async () => {
  try {
    if (!token.value) {
      console.error("Người dùng chưa đăng nhập.");
      return;
    }

    await axios.post(`${API_BASE_URL}/logout/`, {}, {
      headers: {
        Authorization: `Bearer ${token.value}`,
      },
    });

    console.log("Đăng xuất thành công!");
    localStorage.removeItem("token");
    token.value = null;
    userInfo.value = null;
    isLoggedIn.value = false;
    clearUserInfoFromLocalStorage();
    window.location.href = "/dang-nhap/";
  } catch (error) {
    console.error("Lỗi khi đăng xuất:", error);
  }
};

const handleSelectComic = (comicId: string) => {
  navigateTo(`/truyen-tranh/${comicId}`);
  searchInput.value.blur();
};

const handleSearchComics = () => {
  if (!searchValue.value.trim()) return;
  openSidebar.value = false;
  searchInput.value.blur();
  navigateTo(`/search?keyword=${searchValue.value.replace(/\s+/g, '+')}`);
};

watch(openSidebar, (status) => {
  document.body.style.overflow = status ? 'hidden' : 'auto';
});

watch(searchValue, async (newValue) => {
  if (!newValue.trim()) {
    suggestComics.value = [];
    showSuggest.value = false;
    return;
  }

  // Tìm kiếm và lấy kết quả ngay lập tức
  const result = await useFetchData(
    `/tim-kiem?keyword=${newValue.replace(/\s+/g, '+')}`
  );

  suggestComics.value = result.data.items;
  showSuggest.value = suggestComics.value.length > 0;
});

const getScreenWidth = () => {
  const width = window.innerWidth;
  device.value = width >= 1024 ? 'laptop' : 'mobile';
};

onMounted(() => {
  getScreenWidth();
  window.addEventListener('resize', getScreenWidth);
});
onBeforeUnmount(() => {
  window.removeEventListener('resize', getScreenWidth);
});
</script>

<template>
  <header class="shadow bg-[#2dce89] relative z-50">
    <nav
      class="max-w-7xl h-12 md:h-14 mx-auto flex items-center justify-between px-3"
    >
      <div class="flex items-center gap-2 h-full">
        <NuxtLink to="/" class="flex items-center gap-2 h-full select-none">
          <p class="text-white font-bold text-lg">TOGETHER</p>
        </NuxtLink>
      </div>
      <div class="items-center gap-2 text-lg ml-6 text-base hidden lg:flex">
        <div v-for="route in routes.slice(0, 4)" :key="route.path">
          <NuxtLink
          :to="route.path"
          class="px-4 py-2 font-bold hover:duration-150 hover:bg-white hover:text-[#2dce89] text-white items-center rounded-full  "
          active-class="border-2 border-white rounded-full text-[#2dce89]"
          >
          <Icon :name="route.icon" size="24" 
          class=""
          active-class="bg-white rounded-full text-[#2dce89] " />
          {{ route.name }}
          </NuxtLink>
        </div>
      </div>
      <div v-if="device === 'laptop'" class="items-center gap-3 flex">
        <form
          class="flex items-center rounded-full border py-2 focus-within:border-[#2dce89] duration-100 mx-4 relative bg-white"
          @submit.prevent="handleSearchComics"
        >
          <input
            type="text"
            class="outline-none text-sm pl-3 rounded-full"
            placeholder="Search "
            v-model="searchValue"
            ref="searchInput"
            @focus="showSuggest = suggestComics.length > 0"
            @blur="showSuggest = false"
          />
          <button type="submit" class="flex items-center px-3">
            <Icon name="iconamoon:search-bold" />
          </button>
          <ul
            class="z-10 absolute top-11 left-1/2 -translate-x-1/2 w-72 h-max max-h-80 overflow-auto shadow rounded bg-white"
            v-show="showSuggest"
          >
            <li
              v-for="comic in suggestComics"
              :key="comic.id"
              @mousedown="handleSelectComic(comic.id)"
              class="flex gap-2 p-2 border-b hover:bg-gray-200 duration-100 cursor-pointer"
            >
              <img
                :src="'https://otruyenapi.com/uploads/comics/' + comic.thumb_url"
                :alt="comic.name"
                class="border border-[#2dce89] w-16 h-24 object-cover object-center rounded"
              />
              <div>
                <h6 class="font-bold text-sm">
                  {{ comic.name }}
                  <span class="font-normal">
                    ({{ comic.lastest_chapter }})
                  </span>
                </h6>
                <p
                  class="text-sm font-bold text-[#2dce89] flex items-center gap-1"
                >
                  <template v-if="comic.author === 'Đang cập nhật'">
                    <Icon name="mdi:dots-circle" size="16" />
                    Đang cập nhật
                  </template>
                  <template v-else>
                    {{ comic.author.join(' | ') }}
                  </template>
                </p>
                <p class="text-xs font-semibold flex items-center">
                  <template v-for="genre in comic.category">
                    {{ genre.name }} |
                  </template>
                </p>
              </div>
            </li>
          </ul>
        </form>
      </div>
      <div v-else>
        <button @click="openSidebar = true">
          <Icon name="carbon:menu" class="text-white" size="32" />
        </button>
        <div
          :class="`fixed inset-0 bg-[rgba(0,0,0,0.85)] duration-200 ${
            openSidebar
              ? 'opacity-100 pointer-events-auto'
              : 'opacity-0 pointer-events-none'
          }`"
          @click="
            (e) => {
              if (e.currentTarget !== e.target) return;
              openSidebar = false;
            }
          "
        >
          <div
            :class="`absolute right-0 inset-y-0 bg-white p-5 pt-3 w-11/12 max-w-sm duration-200 ${
              openSidebar ? 'translate-x-0' : 'translate-x-full'
            }`"
          >
              <button
                class="ml-auto block w-max mb-2"
                @click="openSidebar = false"
              >
                <Icon name="ep:close-bold" size="28" />
              </button>
            
              <form
                class="flex items-center rounded-full border py-2 focus-within:border-[#2dce89] duration-100 mx-4 relative justify-between bg-white"
                @submit.prevent="handleSearchComics"
              >
                <input
                  type="text"
                  class="outline-none text-sm pl-3 rounded-full "
                  placeholder="Search "
                  v-model="searchValue"
                  ref="searchInput"
                  @focus="showSuggest = suggestComics.length > 0"
                  @blur="showSuggest = false"
                />
                <button type="submit" class="flex items-center px-3">
                  <Icon name="iconamoon:search-bold" />
                </button>
                <ul
                  class="z-10 absolute top-11 left-1/2 -translate-x-1/2 w-72 h-max max-h-80 overflow-auto shadow rounded bg-white"
                  v-show="showSuggest"
                >
                  <li
                    v-for="comic in suggestComics"
                    :key="comic.id"
                    @mousedown="handleSelectComic(comic.id)"
                    class="flex gap-2 p-2 border-b hover:bg-gray-200 duration-100 cursor-pointer"
                  >
                    <img
                      :src="'https://otruyenapi.com/uploads/comics/' + comic.thumb_url"
                      :alt="comic.name"
                      class="border border-[#2dce89] w-16 h-24 object-cover object-center rounded"
                    />
                    <div>
                      <h6 class="font-bold text-sm">
                        {{ comic.name }}
                        <span class="font-normal">
                          ({{ comic.lastest_chapter }})
                        </span>
                      </h6>
                      <p
                        class="text-sm font-bold text-[#2dce89] flex items-center gap-1"
                      >
                        <template v-if="comic.author === 'Đang cập nhật'">
                          <Icon name="mdi:dots-circle" size="16" />
                          Đang cập nhật
                        </template>
                        <template v-else>
                          {{ comic.author.join(' | ') }}
                        </template>
                      </p>
                      <p class="text-xs font-semibold flex items-center">
                        <template v-for="genre in comic.category">
                          {{ genre.name }} |
                        </template>
                      </p>
                    </div>
                  </li>
                </ul>
              </form>

              <ul class="grid gap-3 text-lg font-semibold h-[500px] overflow-y-auto pt-3 boder-radius">
                <NuxtLink
                  to="/"
                  class="p-1 "
                  active-class="text-white bg-[#2dce89]"
                  @click="openSidebar = false"
                >
                  <Icon name="ion:home-outline" size="20" class="mr-1" />
                  Home
                </NuxtLink>
                <NuxtLink
                  to="/genres"
                  class="p-1 "
                  active-class="text-white bg-[#2dce89]"
                  @click="openSidebar = false"
                >
                  <Icon name="fa-solid:list" size="20" class="mr-1" />
                  Thể loại
                </NuxtLink>
                <NuxtLink
                  to="/danh-sach/truyen-moi"
                  class="p-1 "
                  active-class="text-white bg-[#2dce89]"
                  @click="openSidebar = false"
                >
                  <Icon name="fa-solid:star" size="20" class="mr-1" />
                  Truyện mới
                </NuxtLink>
                <NuxtLink
                  to="/danh-sach/sap-ra-mat"
                  class="p-1 "
                  active-class="text-white bg-[#2dce89]"
                  @click="openSidebar = false"
                >
                  <Icon name="fa-solid:hourglass-start" size="20" class="mr-1" />
                  Sắp ra mắt
                </NuxtLink>
                <NuxtLink
                  v-for="route in dynamicRoutes"
                  :key="route.path"
                  :to="route.path"
                  class="p-1 "
                  active-class="text-white bg-[#2dce89]"
                  @click="openSidebar = false"
                >
                <Icon name="fa-solid:caret-right" size="24" 
                class=""
                active-class="border-2 border-white rounded-full text-white" />
                  {{ route.title }}
                </NuxtLink>
              </ul>
              <div class="items-center gap-2 text-lg ml-6 text-base lg:flex">
                <NuxtLink
                :to="routes[4].path"
                class="px-4 py-2 font-bold hover:duration-150 hover:bg-white hover:text-[#2dce89] items-center rounded-full  "
                active-class="border-2 border-white rounded-full text-[#2dce89]"
                >
                <Icon :name="routes[4].icon" size="24" 
                class=""
                active-class="border-2 border-white rounded-full text-[#2dce89] " />
                Login
                </NuxtLink>
            </div>
          </div>
        </div>
      </div>

      <div class="items-center gap-2 text-lg text-base hidden lg:flex">
        <template v-if="isLoggedIn">
          <div class="w-12 h-12 border-4 border-white rounded-full overflow-hidden">
            <NuxtLink 
              :to="routes[5].path">
              <img
                src="../assets/img/team-2.jpg"
                class="w-full h-full object-cover"
              />
            </NuxtLink>
          </div>
          <NuxtLink
            @click="handleLogout"
            class="px-2 py-1 font-bold hover:duration-150 hover:bg-white hover:text-[#2dce89] text-white items-center rounded-full"
            active-class="border-2 border-white rounded-full text-[#2dce89]"
            >
            <Icon :name="routes[6].icon" size="30" 
            class=""
            active-class="border-2 border-white rounded-full text-[#2dce89] " />
          </NuxtLink>
        </template>
        <template v-else>
          <NuxtLink
          :to="routes[4].path"
          class="px-2 py-1 font-bold hover:duration-150 hover:bg-white hover:text-[#2dce89] text-white items-center rounded-full"
          active-class="border-2 border-white rounded-full text-[#2dce89]"
          >
          <Icon :name="routes[4].icon" size="30" 
          class=""
          active-class="border-2 border-white rounded-full text-[#2dce89] " />
          Login
          </NuxtLink>
        </template>
      
      </div>
    </nav>
  </header>
</template>

<style scoped>
@font-face {
  font-family: Chocopy;
  src: url(@/assets/fonts/chocopy.ttf);
}

.chocopy {
  font-family: Chocopy, sans-serif;
}
</style>
