<script lang="ts" setup>
import { type Comic } from '@/types';
import { historyDeleteComic } from '@/utils/localDb';

const props = defineProps<{
  comic: Comic & { last_reading?: string; chapter_id?: number };
  detail?: boolean;
  isHistory?: boolean;
}>();
const { comic, detail, isHistory = false } = props;
const {
  origin_name,
  _id,
  slug,
  status,
  thumb_url,
  name,
  updatedAt,
  chapter_id,
  last_reading,
} = comic;

const isImageLoaded = ref<boolean>(false);
const emit = defineEmits(['delete-comic']);

const handleClickCard = (e: Event, type: 'detail' | 'delete' | 'continue') => {
  e.stopPropagation();
  if (type === 'delete') {
    historyDeleteComic(_id);
    emit('delete-comic', _id);
    return;
  }
  if (type === 'continue') {
    navigateTo(`/truyen-tranh/${slug}/${chapter_id}`);
    return;
  }
  navigateTo(`/truyen-tranh/${slug}`);
};

const baseUrl = 'https://otruyenapi.com/uploads/comics/';
const imageFile = ref(thumb_url);

const imageSrc = computed(() =>`${baseUrl}${imageFile.value}`);
</script>

<template>
  <div
    class="overflow-hidden rounded-md duration-500 border-2 border-transparent  relative group md:group-hover:shadow-md cursor-pointer"
    @click="(e) => handleClickCard(e, 'detail')"
  >
    <div
      class="flex gap-1 absolute font-semibold top-0 inset-x-0 z-10 text-xs text-white"
    >
      <span
        v-if="status === 'Completed'"
        class="bg-sky-500 py-0.5 px-2 rounded-b-sm first:rounded-bl-none"
      >
        End
      </span>
      <span
        v-if="
          updatedAt?.includes('trước') &&
          Number(updatedAt.match(/\d+/)?.[0]) <= 3
        "
        class="bg-amber-400 py-0.5 px-2 rounded-b-sm first:rounded-bl-none"
      >
        Up
      </span>
    </div>
    <div class="relative">
      <div
        :class="`absolute inset-0 flex items-center justify-center text-white bg-gray-200 duration-150 ${
          isImageLoaded ? 'hidden' : 'block'
        }`"
      >
        <Icon name="line-md:loading-loop" size="48" />
      </div>
      <img
        :src="imageSrc"
        :alt="name"
        class="w-full aspect-[2/3] object-cover object-center scale-[1.01] group-hover:scale-105 duration-300 origin-bottom select-none"
        loading="lazy"
        @load="isImageLoaded = true"
      />
    </div>
    <div
      class="absolute top-1/2 bottom-0 inset-x-0 flex flex-col justify-end px-2 sm:px-4 py-2 bg-gradient-to-b from-transparent to-slate-500"
    >
      <h5
        class="font-bold leading-5 text-lg text-white text-shadow duration-200 line-clamp-2"
      >
        <abbr :name="name" class="no-underline">{{ name }}</abbr>
      </h5>
      <template v-if="detail">
        <hr class="mt-3 mb-0.5 border-gray-500" />
        <div>
          <p class="text-sm text-gray-300 truncate font-semibold">
            <template v-if="Array.isArray(origin_name)">
              {{ origin_name.join(' | ') }}
            </template>
            <template v-else-if="origin_name === 'Updating'">
              <span class="flex items-center gap-1">
                <Icon
                  name="mdi:dots-circle"
                  size="16"
                  class="text-emerald-500"
                />
                Updating
              </span>
            </template>
            <template v-else>{{ origin_name }} </template>
          </p>
          <div
            class="hidden md:flex items-center gap-0.5 justify-center gap-x-2 gap-y-1 text-emerald-400 text-xs py-1 mt-0.5"
            v-if="!isHistory"
          >
          </div>
          <div v-else class="text-gray-300">
            <p
              class="text-sm font-semibold flex items-center gap-0.5 mb-1 text-fuchsia-400"
            >
              <Icon name="ph:read-cv-logo-fill" size="18" />
              {{ last_reading }}
            </p>
            <div class="flex items-center gap-1 text-sm text-white">
              <button
                class="bg-sky-500 w-full px-2 py-1 rounded-sm flex justify-center items-center gap-1"
                @click="(e) => handleClickCard(e, 'continue')"
              >
                <Icon name="system-uicons:book-text" size="20" />
                Continue
              </button>
              <button
                class="bg-rose-500 px-2 py-1 rounded-sm"
                @click="(e) => handleClickCard(e, 'delete')"
              >
                <Icon name="ion:trash" size="20" />
              </button>
            </div>
          </div>
        </div>
      </template>
      <span v-else class="py-1" />
    </div>
  </div>
</template>

<style scoped>
.group:hover .text-shadow {
  text-shadow: 0 0 6px #10b981;
}
</style>
