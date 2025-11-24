<script lang="ts" setup>
import { type UserInfo } from "@/types";
import ProfileCard from "@/components/ProfileCard.vue";
import { getUserInfoFromLocalStorage } from '@/utils/localDb';
import axios from "axios";
import { ref, onMounted } from 'vue';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;
const userInfo = ref<UserInfo | null>(getUserInfoFromLocalStorage());
const userInfoShow = ref<any>(getUserInfoFromLocalStorage());

const historyList = ref<any>([]); 
const activeComics = ref<any[]>([]); 
const comicDetails = ref<any[]>([]); 
const historyDetails = ref<any[]>([]); 

onMounted(async () => {
  if (userInfo.value && userInfo.value.email) {
    try {

      //Lấy dữ liệu truyện yêu thích
      const response  = await axios.get(`${API_BASE_URL}/get_favorite_list`, {
        params: {
          email: userInfo.value.email,
        },
      });      
      const data = response.data.data;

      activeComics.value = data.filter((item: { status: boolean }) => item.status === true);
      const comicDetailsPromises = activeComics.value.map((comic: { id_comic: string }) =>
        useFetchData(`/truyen-tranh/${comic.id_comic}`)
      );
      const comicDetailsResponses = await Promise.all(comicDetailsPromises);
      comicDetails.value = comicDetailsResponses.map((response: any) => response.data.item);


      //Lấy dữ liệu lịch sử đọc truyện
      const responseHistory = await axios.get(`${API_BASE_URL}/get_history_comics`, {
        params: {
          email: userInfo.value?.email,
        },
      });
      const data_history = responseHistory?.data?.data;

      historyList.value = data_history;
      const histortDetailsPromises = historyList.value.map((comic: { id_comic: string }) =>
        useFetchData(`/truyen-tranh/${comic.id_comic}`)
      );
      const historyDetailsResponses = await Promise.all(histortDetailsPromises);
      historyDetails.value = historyDetailsResponses.map((responseHistory: any) => responseHistory.data.item);

    } catch (error) {
      console.error("Error fetching favorite list or comic details:", error);
    }
  }
});

const baseUrl = 'https://otruyenapi.com/uploads/comics/';

</script>


<template>
  <main>
    <div class="py-4 container mx-auto">
      <div class="flex flex-wrap">
        <!-- Left Column -->
        <div class="w-full lg:w-1/2 xl:w-3/4 mb-4 p-5">
          <div class="card bg-white shadow-lg rounded-lg pt p-10">
            <div class="card-header pb-0">
              <div class="flex items-center justify-between">
                <p class="mb-0 text-xl font-semibold">User Information</p>
                <button color="success" size="sm" class=" p-2 py-2 bg-[#2dce89] text-white font-semibold rounded-lg hover:bg-[#2dce80] focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-opacity-50">
                  Settings
                </button>
              </div>
            </div>
            <div class="card-body">
              <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label for="username" class="form-control-label text-sm">Username</label>
                  <input class="w-full mt-2 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500" type="text" 
                  v-model="userInfoShow.username" id="username"
                  readonly
                   />
                </div>
                <div>
                  <label for="email" class="form-control-label text-sm">Email address</label>
                  <input class="w-full mt-2 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500" type="email" 
                  v-model="userInfoShow.email" id="email" 
                  readonly
                  />
                </div>
              </div>
              <hr class="my-4 border-t-2 border-gray-300" />
              <p class="text-uppercase text-sm font-medium">Contact Information</p>
              <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
                <div>
                  <label for="address" class="form-control-label text-sm">Address</label>
                  <input class="w-full mt-2 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                    type="text"
                    value="27 Nguyễn Văn Săng, Tân Sân Nhì, Tân Phú"
                    id="address"
                    readonly
                  />
                </div>
                <div>
                  <label for="city" class="form-control-label text-sm">City</label>
                  <input class="w-full mt-2 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500" type="text" 
                  value="Hồ Chí Minh" id="city" readonly />
                </div>
                <div>
                  <label for="country" class="form-control-label text-sm">Country</label>
                  <input class="w-full mt-2 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500" type="text" 
                  value="Việt Nam" id="country" readonly />
                </div>
              </div>
              <hr class="my-4 border-t-2 border-gray-300" />
              <p class="text-uppercase text-sm font-medium">About me</p>
              <div>
                <input class="w-full mt-2 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                  type="text"
                  value="Nghiện đọc truyện, nhất là truyện Doraemon và Pokemon"
                  id="about_me"
                  readonly
                />
              </div>
            </div>
          </div>
        </div>

        <!-- Right Column (Profile Card) -->
        <div class="w-full lg:w-1/2 xl:w-1/4 mb-4">
          <profile-card />
        </div>
      </div>
      <div class="card bg-white shadow-lg rounded-lg pt p-10">
        <p class="mb-3 text-xl font-semibold">Favorite List</p>
        <Swiper
          :slides-per-view="6"
          :space-between="10"
        >
          <SwiperSlide v-for="comic in comicDetails" :key="comic.item">
            <ComicCard :comic="comic" :detail="false" />
          </SwiperSlide>
        </Swiper>
      </div>

      <div class="card bg-white shadow-lg rounded-lg mt-5 p-10">
        <p class="mb-3 text-xl font-semibold">History List</p>
        <Swiper
          :slides-per-view="6"
          :space-between="10"
        >
          <SwiperSlide v-for="comic in historyDetails" :key="comic.item">
            <ComicCard :comic="comic" :detail="false" />
          </SwiperSlide>
        </Swiper>
      </div>
      
    </div>
  </main>
</template>
