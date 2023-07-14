<script setup lang="ts">
import { onBeforeMount, reactive } from "vue";
import { useRoute, useRouter } from "vue-router";

import RippleButton from "@/elements/Button/RippleButton.vue";

import { userState } from "@/state/user";

const route = useRoute();
const router = useRouter();

const state = reactive({
  email: undefined,
  password: undefined,
  remembered: false,
  wrong: false,
});

function submit() {
  const redirect = (route.query.redirect ? route.query.redirect : "/") as string;
  state.wrong = false;

  const formData = new FormData();
  formData.append("username", state.email);
  formData.append("password", state.password);

  userState
    .signIn(formData)
    .then(() => {
      router.push(redirect);
    })
    .catch(() => {
      state.wrong = true;
      state.password = "";
    });
}

onBeforeMount(() => {
  document.addEventListener.call(window, "keyup", (event) => {
    if (event.keyCode === 13 || event.keyCode === 108) {
      submit();
    }
  });
});
</script>

<template>
  <div class="w-full h-100v flex flex-col items-center justify-center">
    <div class="w-96 h-120 flex flex-col rounded-lg border-white shadow-black bg-gray-900">
      <div class="mx-auto text-white text-4xl mt-10">
        <h1>ZetsuBou</h1>
      </div>
      <div class="mt-8 px-6">
        <input type="hidden" name="remember" value="true" />
        <div class="rounded-md shadow-sm -space-y-px text-white">
          <div class="py-1">
            <label class="my-1 inline-block" for="email-address">Email address</label>
            <input
              class="rounded-lg relative block w-full px-3 py-2 border-2 border-gray-700 bg-gray-600 placeholder-gray-400 rounded-t-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm"
              :class="state.wrong ? 'border-2 border-red-700 animate-shake-horizontal' : ''"
              id="email-address"
              name="email"
              type="email"
              autocomplete="email"
              required="true"
              placeholder="Email address"
              v-model="state.email" />
          </div>
          <div class="py-1">
            <label class="my-1 inline-block" for="password">Password</label>
            <input
              class="rounded-lg relative block w-full px-3 py-2 border-2 border-gray-700 bg-gray-600 placeholder-gray-400 rounded-b-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm"
              :class="state.wrong ? 'border-2 border-red-700 animate-shake-horizontal' : ''"
              id="password"
              name="password"
              type="password"
              autocomplete="current-password"
              required="true"
              placeholder="Password"
              v-model="state.password" />
          </div>
        </div>
        <div class="flex items-center justify-between my-4">
          <div class="flex items-center">
            <!-- <input
              id="remember-me" name="remember-me" type="checkbox"
              class="h-4 w-4 text-indigo-600 focus:ring-gray-600 border-gray-700 rounded"
              v-model="state.remembered"
            />
            <label for="remember-me" class="block text-sm text-gray-200 ml-2">
              Remember me
            </label> -->
          </div>
          <div class="text-sm">
            <a href="#" class="font-medium text-indigo-600 hover:text-indigo-500"> Forgot your password? </a>
          </div>
        </div>
        <div>
          <ripple-button
            type="submit"
            class="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-500 hover:bg-indigo-700 focus:outline-none"
            @click="submit">
            <span class="absolute left-0 inset-y-0 flex items-center pl-3">
              <LockClosedIcon class="h-5 w-5 text-indigo-500 group-hover:text-indigo-400" aria-hidden="true" />
            </span>
            Sign in
          </ripple-button>
        </div>
        <div class="mt-2">
          <span class="text-red-500" v-if="state.wrong">
            The username and password you entered did not match our records. Please double-check and try again.
          </span>
        </div>
      </div>
    </div>
  </div>
</template>
