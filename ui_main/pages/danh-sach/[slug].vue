<script lang="ts" setup>
import { topRoutes, filterValues } from '@/utils/data';
import { type Comic, type Genres } from '@/types';

const currentTab = ref<string>('all');
const filterValue = ref<string>('');
const comics = ref<Comic[]>([]);
const totalPages = ref<number>(1);
const isFetching = ref<boolean>(false);
  let comicsData = ref<any>();

const route = useRoute();
const router = useRouter();
const slug = route.params.slug as string;

const [
    lists
  ] = await Promise.all([
      useFetchData(`/danh-sach/${slug}`),
    ]);

const list = lists.data.items;

comicsData = list;

const handleChangeFilter = async (filterId: string) => {
  filterValue.value = filterId;
  const data = await getComics(filterValue.value, p);
  
  comicsData = data;
  
  router.replace({ query: { filter: filterId } });
};

const getComics = async (filterId: string, page: number) => {
  try {
    isFetching.value = true;
    const data_all = list;
    const data_status = list.filter((item: Genres) => item.status === filterId);
    if(filterId == 'all'){
      return data_all;
    }else{
      return data_status;
    }

  } catch (err) {
    console.log(err);
  } finally {
    isFetching.value = false;
  }
};

const currentQuery = route.query.tab as string;
currentTab.value =
  topRoutes.findIndex((r) => r.type === currentQuery) > -1
    ? currentQuery
    : 'all';
const page = route.query.page;
const p = page && !isNaN(+page) ? Number(route.query.page) : 1;
const currentFilter = route.query.filter as string;
filterValue.value =
  filterValues.findIndex((r) => r.value === currentFilter) > -1
    ? currentFilter
    : 'all';
const data = await getComics(currentTab.value, p);
if (!data) {
  throw createError({ statusCode: 404, statusMessage: 'Page Not Found' });
}

const handleChangeTab = (tab: string) => {
  currentTab.value = tab;
  const { page, ...query } = route.query;
  router.replace({
    query: {
      ...query,
      tab,
    },
  });
};



watch([currentTab, route], async ([newTab, route]) => {
  window.scrollTo({ top: 0, behavior: 'smooth' });
  const page = route.query.page || 1;
  await getComics(newTab, Number(page));
});

</script>

<template>
  <Head>
    <Title>STORIES | Free comic and manga reader online</Title>
  </Head>
  <main class="max-w-6xl mx-auto px-3">
    <ul
      class="flex items-center flex-wrap gap-2.5 mb-5 mt-3 font-semibold sm:gap-5"
    >
      <li
        v-for="item in filterValues"
        :class="`min-w-[60px] cursor-pointer text-center border px-3 py-1.5 rounded ${
          item.value === filterValue
            ? 'border-emerald-500 text-emerald-500'
            : ''
        }`"
        @click="handleChangeFilter(item.value)"
      >
        {{ item.label }}
      </li>
    </ul>
    <ComicsPagination
      :comics="comicsData"
      :total-pages="totalPages"
      :is-fetching="isFetching"
    />
  </main>
</template>