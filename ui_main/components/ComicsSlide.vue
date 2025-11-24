<script lang="ts" setup>
type ComicsSlideProps = {
  comics: any;
  title: string;
  icon: string;
  link: string;
};

const props = defineProps<ComicsSlideProps>();
const { comics, title, icon, link } = props;
</script>

<template>
  <div class="flex items-center justify-between mb-4 mt-6 md:mt-12">
    <h2
      class="flex items-center gap-2 text-xl sm:text-2xl md:text-3xl font-bold"
    >
      <Icon :name="icon" size="36" class="text-slate-500" />
      {{ title }}
    </h2>
    <NuxtLink
      :to="link"
      class="btn-more"
    >
    <div class="svg-wrapper-1">
      <div class="svg-wrapper">
        <svg  xmlns="http://www.w3.org/2000/svg"  width="24"  height="24"  viewBox="0 0 24 24"  fill="none"  stroke="currentColor"  stroke-width="2"  stroke-linecap="round"  stroke-linejoin="round"  class="icon icon-tabler icons-tabler-outline icon-tabler-dots"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><path d="M5 12m-1 0a1 1 0 1 0 2 0a1 1 0 1 0 -2 0" /><path d="M12 12m-1 0a1 1 0 1 0 2 0a1 1 0 1 0 -2 0" /><path d="M19 12m-1 0a1 1 0 1 0 2 0a1 1 0 1 0 -2 0" /></svg>
      </div>
    </div>
    <span>Thêm</span>
    </NuxtLink>
  </div>
  <Swiper
    :slides-per-view="5"
    :navigation="true"
    :space-between="20"
    :modules="[SwiperGrid, SwiperNavigation]"
    :breakpoints="{
      0: {
        slidesPerView: 1,
        spaceBetween: 10,
        grid: {
          rows: 1,
        },
      },
      320: {
        slidesPerView: 2,
        spaceBetween: 10,
        grid: {
          rows: 1,
        },
      },
      576: {
        slidesPerView: 3,
        spaceBetween: 10,
        grid: {
          rows: 1,
        },
      },
      768: {
        slidesPerView: 4,
        spaceBetween: 15,
        grid: {
          rows: 2,
          fill: 'row',
        },
      },
      1024: {
        slidesPerView: 5,
        grid: {
          rows: 2,
          fill: 'row',
        },
      },
    }"
    :grid="{
      rows: 2,
      fill: 'row',
    }"
  >
    <SwiperSlide v-for="comic in comics" :key="comic.item">
      <ComicCard :comic="comic" :detail="true" />
    </SwiperSlide>
  </Swiper>
</template>
