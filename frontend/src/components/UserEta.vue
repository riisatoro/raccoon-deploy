<script>
import axios from "axios";
import moment from "moment";
import {onMounted, ref} from "vue";
import {useUserStore} from "../store";

export default {
  setup() {
    const eta = ref({current: null, closed: []});
    const message = ref("");
    const formatDate = (date) => date ? moment(date).format("MM/DD hh:mm a") : "-";

    const fetchUserEta = async () => await axios.get("eta/my/").then((response) => eta.value = response.data);
    const sendEtaCommand = async (payload) => await axios.post("eta/my/", payload).catch(({response}) => message.value = response.data.detail);

    onMounted(
      async () => {
        const store = useUserStore();
        if (store.isAuthenticated) {
          await fetchUserEta();
        }
      }
    );

    const submit = async (e) => {
      const form = new FormData(e.target);
      const payload = Object.fromEntries(form.entries());
      await sendEtaCommand(payload);
      await fetchUserEta();
      message.value = "";

    };

    return {eta, message, formatDate, submit};
  },
};
</script>

<template>
  <div class="m-5">
    <div v-if="eta?.current" class="flex justify-center lg:px-8">
      <table class="min-w-full">
        <thead class="border-b">
          <tr>
            <th scope="col" class="px-6 py-4 text-center text-sm font-bold text-gray-900">Current ETA</th>
            <th scope="col" class="px-6 py-4 text-center text-sm font-medium text-gray-900">Project</th>
            <th scope="col" class="px-6 py-4 text-center text-sm font-medium text-gray-900">Issue</th>
            <th scope="col" class="px-6 py-4 text-center text-sm font-medium text-gray-900">Created at</th>
            <th scope="col" class="px-6 py-4 text-center text-sm font-medium text-gray-900">Expected at</th>
          </tr>
        </thead>
        <tbody>
          <tr class="border-b">
            <td class="whitespace-nowrap px-6 py-4 text-center text-sm font-medium text-gray-900" />
            <td class="whitespace-nowrap px-6 py-4 text-center text-sm font-medium text-gray-900">
              {{
                eta.current.project.name
              }}
            </td>
            <td class="whitespace-nowrap px-6 py-4 text-center text-sm font-medium text-gray-900">
              {{ eta.current.issue
              }}
            </td>
            <td class="whitespace-nowrap px-6 py-4 text-center text-sm font-medium text-gray-900">
              {{
                formatDate(eta.current.created_at)
              }}
            </td>
            <td class="whitespace-nowrap px-6 py-4 text-center text-sm font-medium text-gray-900">
              {{
                formatDate(eta.current.expected_at)
              }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="my-10">
      <form class="flex justify-center" @submit.prevent="submit">
        <input
          type="text" placeholder="ETA command" name="command"
          class="rounded-lg border border-gray-300 bg-gray-50 px-5 py-3 text-sm text-gray-900 focus:border-blue-500 focus:ring-blue-500"
        >
        <button class="m-2 rounded-lg border border-green-500 bg-green-500 px-3 py-2 text-white">OK</button>
      </form>
      <p class="mt-2 text-center text-sm text-red-600">{{ message }}</p>
    </div>

    <h2 v-if="!eta?.closed?.length" class="mt-5 text-center text-lg">You don't have closed ETA for now.</h2>
    <div class="flex justify-center">
      <table class="min-w-full lg:px-8">
        <thead class="border-b">
          <tr>
            <th scope="col" class="px-6 py-4 text-center text-sm font-bold text-gray-900">Closed ETA</th>
            <th scope="col" class="px-6 py-4 text-center text-sm font-medium text-gray-900">Project</th>
            <th scope="col" class="px-6 py-4 text-center text-sm font-medium text-gray-900">Issue</th>
            <th scope="col" class="px-6 py-4 text-center text-sm font-medium text-gray-900">Created at</th>
            <th scope="col" class="px-6 py-4 text-center text-sm font-medium text-gray-900">Expected at</th>
            <th scope="col" class="px-6 py-4 text-center text-sm font-medium text-gray-900">Done at</th>
          </tr>
        </thead>
        <tbody v-for="(item) in eta?.closed" :key="item.project.name + item.user.username" class="m-2 text-center">
          <tr class="border-b">
            <td class="whitespace-nowrap px-6 py-4 text-sm font-medium text-gray-900" />
            <td class="whitespace-nowrap px-6 py-4 text-sm font-medium text-gray-900">{{ item.project.name }}</td>
            <td class="whitespace-nowrap px-6 py-4 text-sm font-medium text-gray-900">{{ item.issue }}</td>
            <td class="whitespace-nowrap px-6 py-4 text-sm font-medium text-gray-900">
              {{ formatDate(item.created_at) }}
            </td>
            <td class="whitespace-nowrap px-6 py-4 text-sm font-medium text-gray-900">
              {{ formatDate(item.expected_at) }}
            </td>
            <td class="whitespace-nowrap px-6 py-4 text-sm font-medium text-gray-900">
              {{ formatDate(item.done_at) }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>
