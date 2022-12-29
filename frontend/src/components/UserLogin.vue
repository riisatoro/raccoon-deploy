<script>
import axios from "axios";
import {useRouter} from "vue-router";
import {useUserStore} from "../store";

export default {
  name: "UserLogin",
  setup() {
    const router = useRouter();
    const store = useUserStore();

    const submit = async (e) => {
      const form = new FormData(e.target);
      const payload = Object.fromEntries(form.entries());

      const {data} = await axios.post("token/", payload);
      axios.defaults.headers.common["Authorization"] = `Bearer ${data.access}`;
      window.localStorage.setItem("refresh", data.refresh);
      store.$patch({isAuthenticated: true});
      await router.push("/");
    };

    return {submit};
  },
};
</script>

<template>
  <div class="m-5 text-center">
    <h2>Log in to continue</h2>
    <form @submit.prevent="submit">
      <input name="username" type="text" placeholder="Username" class="mt-5 h-10 rounded-lg border border-gray-300 bg-gray-50 p-2 text-sm text-gray-900 focus:border-blue-500 focus:ring-blue-500">
      <br>
      <input name="password" type="password" placeholder="Password" class="mt-2 h-10 rounded-lg border border-gray-300 bg-gray-50 p-2 text-sm text-gray-900 focus:border-blue-500 focus:ring-blue-500">
      <br>
      <button type="submit" class="my-5 rounded bg-green-500 px-3 py-1 text-white">Login</button>
    </form>
  </div>
</template>
