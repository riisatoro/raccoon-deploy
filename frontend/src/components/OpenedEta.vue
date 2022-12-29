<script>
import axios from "axios";
import moment from "moment";
import {onMounted, ref} from "vue";
import {useRouter} from "vue-router";

export default {
  setup() {
    const router = useRouter();
    const eta = ref([]);
    const formatDate = (date) => date ? moment(date).format("MM/DD hh:mm a") : "-";
    onMounted(
      async () => {
        try {
          await axios.get("eta/").then((response) => eta.value = response.data);
        } catch (e) {
          router.push("/login");
        }
      }
    );
    return {eta, formatDate};
  },
};
</script>

<template>
  <div class="my-5 flex justify-center">
    <table v-if="eta?.length" class="min-w-full lg:px-8">
      <thead class="border-b">
        <tr>
          <th scope="col" class="px-6 py-4 text-center text-sm font-bold text-gray-900">All opened ETA</th>
          <th scope="col" class="px-6 py-4 text-center text-sm font-medium text-gray-900">Project</th>
          <th scope="col" class="px-6 py-4 text-center text-sm font-medium text-gray-900">Issue</th>
          <th scope="col" class="px-6 py-4 text-center text-sm font-medium text-gray-900">Created at</th>
          <th scope="col" class="px-6 py-4 text-center text-sm font-medium text-gray-900">Expected at</th>
        </tr>
      </thead>
      <tbody v-for="(item) in eta" :key="item.project.name + item.user.username" class="m-2 text-center">
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
        </tr>
      </tbody>
    </table>

    <h2 v-if="!eta?.length">No opened ETA for now.</h2>
  </div>
</template>
