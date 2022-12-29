<script>
import axios from "axios";
import moment from "moment";
import {onMounted, ref} from "vue";
import {useUserStore} from "../store";

export default {
  setup() {
    const eta = ref({current: null, closed: []});
    const formatDate = (date) => date ? moment(date).format("MM/DD hh:mm a") : "-";

    onMounted(
      async () => {
        const store = useUserStore();
        if (store.isAuthenticated) {
          await axios.get("eta/my/").then((response) => eta.value = response.data);
        }
      }
    );

    return {eta, formatDate};
  },
};
</script>

<template>
  <div class="m-5">
    <div v-if="eta?.current" class="flex justify-center">
      <table class="m-2 text-center">
        <thead>
          <tr>
            <th />
            <th class="p-2" colspan="2">Project & Issue</th>
            <th class="p-2" colspan="2">Start / Finish time</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td class="border-r-4 p-2">Current ETA</td>
            <td class="p-1">{{ eta.current.project.name }}</td>
            <td class="p-1 px-5">{{ eta.current.issue }}</td>
            <td class="p-2">{{ formatDate(eta.current.created_at) }}</td>
            <td class="p-2">{{ formatDate(eta.current.expected_at) }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="m-2">
      <form class="flex justify-center">
        <input
          type="text" placeholder="ETA command"
          class="rounded-lg border border-gray-300 bg-gray-50 px-5 py-3 text-sm text-gray-900 focus:border-blue-500 focus:ring-blue-500"
        >
        <button class="m-2 rounded-lg border border-green-500 bg-green-500 px-3 py-2 text-white">OK</button>
      </form>
    </div>

    <h2 v-if="eta?.closed?.length" class="mt-5 text-center text-lg">My closed ETA</h2>
    <h2 v-if="!eta?.closed?.length" class="mt-5 text-center text-lg">You don't have closed ETA for now.</h2>
    <div class="flex justify-center">
      <table v-for="(item) in eta?.closed" :key="item.project.name + item.user.username" class="m-2 text-center">
        <tr>
          <td class="border-r-4 p-2" />
          <td class="p-1">{{ item.project.name }}</td>
          <td class="p-1 px-5">{{ item.issue }}</td>
          <td class="p-2">{{ formatDate(item.created_at) }}</td>
          <td class="p-2">{{ formatDate(item.done_at) }}</td>
        </tr>
      </table>
    </div>
  </div>
</template>
