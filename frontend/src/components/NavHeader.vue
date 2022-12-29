<script>
import axios from "axios";
import {useUserStore} from "../store";

export default {
  mounted() {
    if (!this.isAuthenticated()) {
      this.$router.push("/login");
    }
  },
  methods: {
    logout() {
      const store = useUserStore();
      axios.defaults.headers.common["Authorization"] = "";
      store.$patch({isAuthenticated: false});
      this.$router.push("/login");
    },
    isAuthenticated() {
      const store = useUserStore();
      return store.isAuthenticated;
    }

  }
};
</script>

<template>
  <div class="flex items-center justify-center bg-indigo-50">
    <router-link v-if="isAuthenticated()" to="/" class="m-2 cursor-pointer rounded-xl bg-blue-500 px-5 py-3 text-white">My ETA</router-link>
    <router-link v-if="isAuthenticated()" to="/opened" class="m-2 cursor-pointer rounded-xl bg-green-500 px-5 py-3 text-white">Opened ETA</router-link>
    <button v-if="isAuthenticated()" class="m-2 cursor-pointer rounded-xl bg-red-500 px-5 py-3 text-white" @click="logout">Logout</button>
    <hr>
  </div>
</template>
