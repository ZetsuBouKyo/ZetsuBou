<template>
  <div class="relative mx-1">
    <dropdown
      ref="dropdown"
      class="text-white bg-gray-700 border-2 border-gray-600 hover:bg-gray-500 rounded-lg"
      :selectClass="'border-r-2 border-gray-600'">
      <template v-slot:select>
        <button class="focus:outline-none">
          <div
            class="inline-flex items-center h-full"
            :title="progressState.data.title ? progressState.data.title : undefined">
            <svg class="m-1 h-8" viewBox="0 0 80.795341 80.795341">
              <g transform="translate(-45.445339,-324.23139)">
                <path
                  style="fill: #ffffff; stroke-width: 0.26767731"
                  d="m 82.25748,396.70773 c -6.880614,-0.63025 -13.204863,-4.75645 -16.631017,-10.44446 -1.003664,-1.66626 -1.583488,-2.0172 -3.228172,-2.34615 -3.929163,-0.78584 -5.805873,-3.72198 -6.514827,-7.31707 -0.41422,-2.10048 -0.13735,-4.71932 1.264823,-5.83511 l 0.658657,-1.17084 0.236633,-1.65644 c 0.339919,-2.37945 -1.081079,-6.99181 -0.887535,-8.16121 0.123038,-0.7434 0.01691,-1.08957 -0.529095,-1.72581 -1.4504,-1.69006 -3.253878,-5.95771 -3.749134,-8.87173 l -0.192649,-1.13352 1.173866,0.1795 c 0.645626,0.0987 1.934162,0.38407 2.863411,0.63409 0.929249,0.25001 1.689545,0.37724 1.689545,0.28271 0,-0.0946 -0.433902,-0.97306 -0.964227,-1.95231 -0.530325,-0.97924 -0.839077,-1.78044 -0.686116,-1.78044 0.15296,0 1.180782,0.28106 2.284048,0.62458 l 2.005936,0.62458 1.08605,-1.61853 c 6.072385,-9.04961 17.63251,-13.96978 28.690992,-12.21134 16.966461,2.69787 27.831851,18.90535 23.640881,35.2642 -0.40909,1.59681 0.37774,1.00985 1.04011,1.96687 2.101,3.0356 1.82305,8.3946 -1.03829,10.79602 -1.11435,0.93523 -3.7027,3.06988 -4.96017,3.07511 l -1.30108,1.32059 c -0.56466,0.98694 -1.14165,1.94124 -2.67431,3.44431 -2.0701,2.03016 -3.99184,3.82177 -5.952997,4.8164 -1.338114,0.67865 -4.123929,1.9757 -5.095652,2.26638 -2.841306,0.84989 -8.722673,1.1645 -12.229681,0.92962 z m 9.078236,-1.8897 c 6.466015,-1.30636 11.526224,-4.82562 15.042074,-10.46145 0.85874,-1.37653 1.48517,-2.27803 1.39209,-2.00332 -0.15171,0.44767 -0.0571,0.4847 0.91291,0.35713 2.45301,-0.32259 5.1497,-2.37988 6.1538,-4.58429 0.77071,-1.69201 0.68225,-4.86883 -0.0663,-6.3299 -0.29468,-0.57517 -0.65742,-1.08048 -0.8061,-1.1229 -0.14868,-0.0424 -0.61339,0.7537 -1.03269,1.76915 -0.62554,1.51493 -2.92366,5.37309 -3.67141,6.1637 -0.10302,0.10893 -0.13658,-0.58313 -0.0746,-1.5379 0.062,-0.95479 -0.02,-2.41556 -0.18222,-3.24617 -0.16223,-0.83061 -0.36302,-1.92767 -0.44619,-2.4379 -0.41581,-2.55074 -1.77226,-5.86818 -2.88733,-7.06148 -0.29175,-0.31221 -0.55922,-0.7598 -0.59437,-0.99462 -0.16094,-1.07519 -4.30989,-5.95835 -6.090354,-7.16816 l -1.09977,-0.74726 -1.240054,1.02811 c -2.16122,1.79184 -4.635259,3.44754 -6.806454,4.55509 -2.433356,1.24127 -5.904243,2.44198 -7.00987,2.42498 -0.735011,-0.0113 -0.700663,-0.069 0.926227,-1.55703 0.92925,-0.84991 1.689545,-1.62193 1.689545,-1.71557 0,-0.0937 -0.599867,0.12776 -1.333037,0.49204 -0.733168,0.36427 -2.588288,1.07009 -4.122489,1.56847 -3.034206,0.98567 -7.4836,1.54865 -10.267716,1.29917 -1.355801,-0.12148 -1.638181,-0.0571 -2.466796,0.5626 -1.981105,1.48158 -3.777896,7.30525 -3.821827,12.38711 l -0.0198,2.2904 -0.898308,-1.23019 c -1.191007,-1.631 -2.57337,-4.11182 -3.16432,-5.67876 -0.263005,-0.69737 -0.612156,-1.22761 -0.775889,-1.1783 -0.706475,0.21274 -1.315591,2.11045 -1.325852,4.13074 -0.02077,4.09026 2.419461,7.04612 6.572301,7.96099 1.124038,0.24763 1.125454,0.24696 0.961367,-0.45788 -0.09038,-0.38824 0.235807,0.01 0.724864,0.88444 3.732779,6.67606 9.732868,10.90836 16.82874,11.87053 2.117651,0.28715 7.062002,0.15992 8.999775,-0.23157 z M 63.949611,369.46284 c 0.370045,-1.27542 1.10017,-3.15101 1.622499,-4.16799 0.52233,-1.01697 0.949691,-1.91549 0.949691,-1.99672 0,-0.0812 -0.273706,-0.26648 -0.608236,-0.41168 -0.579967,-0.25171 -0.576826,-0.25644 0.06759,-0.10169 0.371699,0.0893 2.318055,0.2233 4.325234,0.29786 3.056074,0.11352 4.110907,0.0427 6.487852,-0.43585 3.038483,-0.61169 6.795858,-1.96152 8.988458,-3.2291 0.742215,-0.42909 1.393323,-0.73719 1.446899,-0.68466 0.131457,0.12889 -2.236972,2.56226 -3.373213,3.4657 -0.501879,0.39905 -0.84418,0.79255 -0.760668,0.87443 0.245294,0.24051 3.659273,-0.95424 5.998411,-2.09919 3.277233,-1.60413 5.108256,-2.92619 8.503511,-6.13986 2.948431,-2.79074 3.252861,-2.96121 1.559387,-0.87321 l -0.750189,0.92496 2.659863,2.61678 c 5.55824,5.46821 8.43713,11.58439 8.43713,17.92455 0,2.12567 0.35907,1.80844 2.28048,-2.01474 3.28062,-6.5277 3.92505,-13.35136 1.90542,-20.17593 -4.47537,-15.12285 -20.991122,-23.77837 -36.082369,-18.90993 -6.098511,1.96738 -11.747145,6.13136 -15.041042,11.08774 l -1.324679,1.99327 -1.887896,-0.71189 c -1.038342,-0.39153 -1.934318,-0.6665 -1.991057,-0.61102 -0.05674,0.0555 0.450929,0.96899 1.128152,2.03003 0.677223,1.06104 1.210235,1.94809 1.184471,1.9712 -0.02577,0.0231 -1.384964,-0.3032 -3.020443,-0.72512 -1.635479,-0.42193 -3.075527,-0.76805 -3.200106,-0.76916 -0.357381,-0.003 0.0835,2.05945 0.92723,4.33802 0.829225,2.2394 2.003889,4.21605 3.432701,5.77631 0.784693,0.85689 0.819673,0.95396 0.295319,0.81951 -0.592166,-0.15184 -0.481983,0.13909 -0.295262,2.74359 0.359169,5.00992 1.519085,8.97963 3.776654,12.71275 l 1.270585,2.10103 0.20741,-2.65053 c 0.114077,-1.45779 0.510175,-3.69405 0.880221,-4.96946 z m -2.623168,3.97583 c -1.915856,-3.85364 -2.914457,-7.69026 -2.914457,-11.19733 0,-1.77061 0.04449,-1.92836 0.510145,-1.80897 0.992627,0.25451 0.862678,-0.46669 -0.289388,-1.60608 -0.641796,-0.63474 -1.583336,-1.83609 -2.092309,-2.66968 -0.976024,-1.5985 -2.453683,-5.38167 -2.453683,-6.28203 0,-0.61088 0.268666,-0.58105 3.839973,0.42644 1.145566,0.32316 2.222702,0.50283 2.393636,0.39925 0.211684,-0.12828 -0.03758,-0.72556 -0.781696,-1.87309 -0.600865,-0.92661 -1.055169,-1.72133 -1.009563,-1.76604 0.04561,-0.0447 0.73697,0.17147 1.536365,0.48041 1.36661,0.52816 1.469649,0.53421 1.72469,0.1012 2.129331,-3.61519 5.694284,-7.4264 8.869945,-9.48267 8.257047,-5.3465 18.713705,-6.05662 27.720169,-1.88249 13.26233,6.14657 19.25564,21.3262 13.8335,35.03697 -0.44753,1.13164 -1.09968,2.51832 -1.44923,3.0815 l -0.63555,1.02397 -0.17288,-2.0052 c -0.4944,-5.73466 -3.38199,-11.27149 -8.47609,-16.25254 -2.428814,-2.3749 -2.470764,-2.43707 -1.954197,-2.89545 0.602187,-0.53433 2.138517,-2.74141 2.138517,-3.07216 0,-0.63705 -0.97965,0.0791 -3.85192,2.81615 -3.407633,3.24711 -6.500279,5.43951 -9.695947,6.8735 -3.326084,1.49253 -3.548195,1.49177 -2.124565,-0.007 2.241985,-2.36071 2.499014,-2.70782 2.3282,-3.14428 -0.142546,-0.36422 -0.332837,-0.31387 -1.318253,0.34886 -2.445661,1.64478 -6.107253,3.10329 -10.207622,4.06599 -2.29967,0.53993 -8.858032,0.46487 -11.450465,-0.13105 -1.583275,-0.36395 -2.202228,-0.41175 -2.430685,-0.18775 -0.375799,0.36847 -0.01131,0.63275 1.716427,1.24457 l 1.216473,0.43077 -1.014992,2.03905 c -1.125233,2.26053 -1.982704,5.27948 -2.294388,8.078 L 62.33173,375.461 Z" />
              </g>
            </svg>
            <div class="w-32 mr-2 hidden lg:flex lg:flex-col">
              <span class="text-left truncate" :class="progressState.data.style ? 'text-sm' : ''">{{
                userState.name
              }}</span>
              <quest-progress />
            </div>
          </div>
        </button>
      </template>
      <template v-slot:options>
        <ripple-button class="flex w-full">
          <router-link class="flex flex-row p-2 w-full hover:bg-gray-600 hover:text-white" to="" @click="close">
            <icon-ic-baseline-person class="self-center ml-2" style="font-size: 1.4rem" />
            <span class="flex px-2 py-1 self-center">Profile</span>
          </router-link>
        </ripple-button>
        <ripple-button class="flex w-full">
          <router-link class="flex flex-row p-2 w-full hover:bg-gray-600 hover:text-white" to="" @click="close">
            <icon-ic-outline-analytics class="self-center ml-2" style="font-size: 1.4rem" />
            <span class="flex px-2 py-1 self-center">Analytics</span>
          </router-link>
        </ripple-button>
        <ripple-button class="flex w-full">
          <router-link
            class="flex flex-row p-2 w-full hover:bg-gray-600 hover:text-white"
            to="/bookmark/gallery"
            @click="close">
            <icon-mdi-bookmark-outline class="self-center ml-2" style="font-size: 1.4rem" />
            <span class="flex px-2 py-1 self-center">Bookmark</span>
          </router-link>
        </ripple-button>
        <ripple-button class="flex w-full">
          <router-link
            class="flex flex-row p-2 w-full hover:bg-gray-600 hover:text-white"
            to="/settings/account"
            @click="close">
            <icon-mdi-user-settings-variant class="self-center ml-2" style="font-size: 1.4rem" />
            <span class="flex px-2 py-1 self-center">Settings</span>
          </router-link>
        </ripple-button>
        <ripple-button class="flex w-full focus:outline-none">
          <a class="flex flex-row p-2 w-full hover:bg-gray-600 hover:text-white" @click="signOut">
            <icon-octicon-sign-out class="self-center ml-2" style="font-size: 1.4rem" />
            <span class="flex px-2 py-1 self-center">Sign Out</span>
          </a>
        </ripple-button>
      </template>
    </dropdown>
  </div>
</template>

<script>
import { reactive, ref } from "vue";

import RippleButton from "@/elements/Button/RippleButton.vue";
import Dropdown from "@/elements/Dropdown/Dropdown.vue";
import { userState } from "@/state/user";

import { progressState } from "./progress";
import QuestProgress from "./QuestProgress.vue";

export default {
  components: { RippleButton, Dropdown, QuestProgress },
  setup() {
    const dropdown = ref();

    const dropdownState = reactive({
      popout: false,
      close: () => {
        dropdownState.popout = false;
      },
      activate: () => {
        dropdownState.popout = true;
      },
      toggle: () => {
        dropdownState.popout = !dropdownState.popout;
      },
    });

    function signOut() {
      userState.signOut();
      window.open("/", "_self");
    }

    progressState.init();

    function close() {
      dropdown.value.close();
    }

    return { userState, dropdown, dropdownState, progressState, signOut, close };
  },
};
</script>
