<script lang="ts" setup>

import { getUserInfoFromLocalStorage } from '@/utils/localDb';
const userInfo = ref<any>(getUserInfoFromLocalStorage());
</script>

<template>
  <div class="card profile-card rounded-lg overflow-hidden shadow-lg">
    <img
      src="../assets/img/bg-profile.jpg"
      alt="Image placeholder"
      class="w-full h-48 object-cover"
    />
    <div class="flex justify-center mt-[-2rem] mb-4">
      <div class="w-24 h-24 border-4 border-white rounded-full overflow-hidden">
        <a href="javascript:;">
          <img
            src="../assets/img/team-2.jpg"
            class="w-full h-full object-cover"
          />
        </a>
      </div>
    </div>
    <div class="text-center pb-4 p-4">
      <div class="flex justify-between mb-4">
        
        <a
          href="javascript:;"
          class="btn btn-sm bg-blue-500 text-white py-2 px-4 rounded-md lg:hidden"
        >
          <i class="ni ni-collection"></i>
        </a>
        
        <a
          href="javascript:;"
          class="btn btn-sm bg-gray-800 text-white py-2 px-4 rounded-md lg:hidden"
        >
          <i class="ni ni-email-83"></i>
        </a>
      </div>
    </div>
    <div class="card-body pt-0">
      <div class="flex justify-center space-x-8">
        <div class="text-center">
          <span class="text-lg font-bold">22</span>
          <span class="text-sm text-opacity-60">Like</span>
        </div>
        <div class="text-center">
          <span class="text-lg font-bold">10</span>
          <span class="text-sm text-opacity-60">Comic</span>
        </div>
        <div class="text-center">
          <span class="text-lg font-bold">89</span>
          <span class="text-sm text-opacity-60">Comments</span>
        </div>
      </div>
      <div class="text-center mt-4">
        <h5 class="text-2xl font-semibold">
          
          <span class="font-light text-xl">{{userInfo.username}}</span>
        </h5>
        <div class="text-lg mt-4 mb-2">
          <i class="ni business_briefcase-24 mr-2"></i>Chúa tể Wibu - Ông Hoàng Anime
        </div>
      </div>
    </div>
  </div>
</template>
