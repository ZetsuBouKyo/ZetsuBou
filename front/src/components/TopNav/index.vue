<template>
  <section class="sticky top-0 shadow-black">
    <header class="text-gray-400 bg-gray-900 body-font xl:px-8 md:px-4 sm:px-2">
      <div class="flex flex-row mx-auto items-center">
        <icon />
        <router-link class="lg:inline hidden ml-8 3xl:text-xl text-lg text-gray-300 hover:text-gray-500" to="/gallery">
          Gallery
        </router-link>
        <router-link class="lg:inline hidden ml-4 3xl:text-xl text-lg text-gray-300 hover:text-gray-500" to="/video">
          Video
        </router-link>
        <nav class="ml-4 flex flex-row items-center text-base justify-center w-full 3xl:text-lg">
          <search class="h-10" />
          <sync class="h-10 md:inline-flex hidden" />

          <user class="h-10" />
        </nav>
      </div>
    </header>
  </section>
</template>

<script lang="ts">
import Sync from "./Sync.vue";
import Search from "./Search.vue";
import Icon from "./Icon.vue";
import User from "./User/index.vue";

export default {
  components: { Sync, Search, Icon, User },
  setup() {},
};
</script>
