<script lang="ts" setup>
import { meta } from '@/utils/data';
import axios from 'axios';

const MyAPI = axios.create({
  baseURL: 'http://134.185.90.103:8080/',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': ``
  },
});

const [
  ancientComicsResponse,
  actionComicsResponse,
  adultComicsResponse,
  adventureComicsResponse,
  animeComicsResponse,
  reincarnationComicsResponse,
] = await Promise.all([
  useFetchData('/the-loai/co-dai'),
  useFetchData('/the-loai/action'),
  useFetchData('/the-loai/adult'),
  useFetchData('/the-loai/adventure'),
  useFetchData('/the-loai/anime'),
  useFetchData('/the-loai/chuyen-sinh'),
]);

const responseTest = await MyAPI.get('/home_client');
// console.log(responseTest)
const dataTest = responseTest.data.items

// Extract the actual comic data from the responses
const ancientComics = ancientComicsResponse.data.items;
const actionComics = actionComicsResponse.data.items;
const adultComics = adultComicsResponse.data.items;
const adventureComics = adventureComicsResponse.data.items;
const animeComics = animeComicsResponse.data.items;
const reincarnationComics = reincarnationComicsResponse.data.items;

useSeoMeta(meta());
useServerSeoMeta(meta());
</script>

<template>
  <main class="max-w-6xl mx-auto py-5 px-3 ">
    <Swiper
      :slides-per-view="6"
      :loop="true"
      :space-between="10"
      :autoplay="{
        delay: 5000,
        disableOnInteraction: false,
      }"
      :modules="[SwiperAutoplay]"
      :breakpoints="{
        0: {
          slidesPerView: 1,
        },
        320: {
          slidesPerView: 2,
        },
        576: {
          slidesPerView: 3,
        },
        768: {
          slidesPerView: 4,
        },
        1024: {
          slidesPerView: 5,
        },
        1280: {
          slidesPerView: 6,
        },
      }"
    >
      <SwiperSlide v-for="comic in adventureComics" :key="comic.item">
        <ComicCard :comic="comic" :detail="false" />
      </SwiperSlide>
    </Swiper>
    <ComicsSlide
      title="Cổ Đại"
      :comics="dataTest"
      icon=""
      link="/the-loai/co-dai"
    />
    <ComicsSlide
      title="Action"
      :comics="actionComics"
      icon=""
      link="/the-loai/action"
    />
    <ComicsSlide
      title="Trưởng thành"
      :comics="adultComics"
      icon=""
      link="/the-loai/adult"
    />
    <ComicsSlide
      title="Phiêu lưu"
      :comics="adventureComics"
      icon=""
      link="/the-loai/adventure"
    />
    <ComicsSlide
      title="Truyện Anime"
      :comics="animeComics"
      icon=""
      link="/the-loai/anime"
    />
    <ComicsSlide
      title="Chuyển sinh"
      :comics="reincarnationComics"
      icon=""
      link="/the-loai/chuyen-sinh"
    />
  </main>
</template>
