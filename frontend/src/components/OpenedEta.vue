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
    <table v-if="eta?.length" class="table-auto">
      <thead>
        <tr>
          <th>Project</th>
          <th>Issue</th>
          <th>Created at</th>
          <th>Expected at</th>
        </tr>
      </thead>
      <tbody v-for="(item) in eta" :key="item.project.name + item.user.username">
        <tr>
          <td class="p-2">{{ item.project.name }}</td>
          <td class="p-2">{{ item.issue }}</td>
          <td class="p-2">{{ formatDate(item.created_at) }}</td>
          <td class="p-2">{{ formatDate(item.expected_at) }}</td>
        </tr>
      </tbody>
    </table>
    <h2 v-if="!eta?.length">No opened ETA for now.</h2>
  </div>
</template>
