<script lang="ts" setup>
import { Comic, Genre, Genres } from 'types';

const currentGenre = ref<string>('');
const comics = ref<Comic[]>([]);
const totalPages = ref<number>(0);
const genres = ref<Genres[]>([]);
const isFetching = ref<boolean>(false);
let comicsData = ref<any>();

const router = useRouter();
const route = useRoute();


const handleChangeGenre = async (genreId: string) => {
  currentGenre.value = genreId;
  const data = await getComics(currentGenre.value, p);
  
  comicsData = data;
  router.replace({
    query: {
      type: genreId,
    },
  });
};

const getComics = async (genreId: string, page: number) => {
  try {
    isFetching.value = true;
    const data = await useFetchData(`/the-loai/${genreId}?page=${page}`);
    comics.value = data?.comics;
    totalPages.value = data?.total_pages;
    return data;
  } catch (err) {
    console.log(err);
  } finally {
    isFetching.value = false;
  }
};

const page = route.query.page;
const p = page && !isNaN(+page) ? Number(route.query.page) : 1;
const type = route.query.type;
currentGenre.value = type ? String(type) : 'all';
const [comicsData_2, genresData] = await Promise.all([
  getComics(currentGenre.value, p),
  useFetchData('/the-loai'),
]);

comicsData = comicsData_2;

const genresItem = genresData.data.items;

const initSlide = genresItem.findIndex(
  (genre: any) => genre.slug === route.query.type
);
if (initSlide === -1 || !comicsData) {
  throw createError({ statusCode: 404, statusMessage: 'Page Not Found' });
}
genres.value = genresItem;

watch(route, async (route) => {
  window.scrollTo({ top: 0, behavior: 'smooth' });
  const page = route.query.page;
  const p = page && !isNaN(+page) ? Number(page) : 1;
  const genre = route.query.type ? String(route.query.type) : 'all';
  await getComics(genre, p);
});
</script>

<template>
  <Head>
    <Title>{{
      `${
        genres.find((genre: any) => genre.slug === currentGenre)?.name +
          ` - Page ${route.query.page ?? 1}` || 'Genres'
      } | STORIES`
    }}</Title>
  </Head>
  <main class="max-w-6xl mx-auto px-3">
    <h2
      class="flex items-center gap-2 text-xl sm:text-2xl md:text-3xl font-bold mb-4 mt-4 md:mt-8"
    >
      Thể loại
    </h2>
    <Swiper
      slides-per-view="auto"
      :loop="false"
      class="border-y"
      :modules="[SwiperFreeMode, SwiperNavigation]"
      :free-mode="true"
      :initial-slide="initSlide"
    >
      <SwiperSlide
        v-for="genre in genresData.data.items"
        :key="genre.slug"
        :class="`swiper-slide-genre px-5 py-3 select-none cursor-pointer ${
          genre.slug === currentGenre ? 'bg-slate-500 text-white' : ''
        }`"
        @click="handleChangeGenre(genre.slug)"
      >
        {{ genre.name }}
      </SwiperSlide>
    </Swiper>
    <p
      class="my-5 flex items-center gap-2 py-2 px-3 rounded bg-sky-500 text-white"
    >
      <Icon
        name="tabler:star"
        size="30"
        class="w-full max-w-[30px]"
      />
        Những câu chuyện ly kỳ, phiêu lưu thú vị
    </p>
    <ComicsPagination
      :comics="comicsData.data.items"
      :total-pages="totalPages"
      :is-fetching="isFetching"
    />
  </main>
</template>

<style scoped>
.swiper-slide-genre {
  width: max-content !important;
}
</style>