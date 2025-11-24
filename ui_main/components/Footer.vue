<template>
  <footer class="bg-white">
    <div class="max-w-7xl px-4 py-12 mx-auto space-y-8 overflow-hidden">
      <div class="flex justify-center mt-8 space-x-6">
        <NuxtLink
          target="_blank"
          rel="noopener noreferrer"
          to=""
          class="text-gray-400 hover:text-gray-500"
        >
          <span class="sr-only">Facebook</span>
          <Icon name="mdi:facebook" size="28" />
        </NuxtLink>
        <NuxtLink
          target="_blank"
          rel="noopener noreferrer"
          to=""
          class="text-gray-400 hover:text-gray-500"
        >
          <span class="sr-only">GitHub</span>
          <Icon name="uil:github" size="28" />
        </NuxtLink>
        <NuxtLink
          target="_blank"
          rel="noopener noreferrer"
          to=""
          class="text-gray-400 hover:text-gray-500"
        >
          <span class="sr-only">API</span>
          <Icon name="mdi:api" size="28" />
        </NuxtLink>
      </div>
      <p class="mt-8 text-base leading-6 text-center text-gray-400 flex justify-center">
        © {{ new Date().getFullYear() }} STORIES
        <svg  xmlns="http://www.w3.org/2000/svg"  
        width="24" 
        height="24"  
        viewBox="0 0 24 24"  
        fill="none"  
        stroke="currentColor" 
         stroke-width="2"  
         stroke-linecap="round"  
         stroke-linejoin="round"  
         class="icon icon-tabler icons-tabler-outline icon-tabler-hearts">
         <path stroke="none" d="M0 0h24v24H0z" fill="none"/>
         <path d="M14.017 18l-2.017 2l-7.5 -7.428a5 5 0 1 1 7.5 -6.566a5 5 0 0 1 8.153 5.784" /><path d="M15.99 20l4.197 -4.223a2.81 2.81 0 0 0 0 -3.948a2.747 2.747 0 0 0 -3.91 -.007l-.28 .282l-.279 -.283a2.747 2.747 0 0 0 -3.91 -.007a2.81 2.81 0 0 0 -.007 3.948l4.182 4.238z" /></svg>. All rights reserved.
      </p>
    </div>
  </footer>
</template>
