<script>
import NavHeader from "./components/NavHeader.vue";
export default {
  name: "App",
  components: {
    NavHeader,
  }
};
</script>

<template>
  <NavHeader />
  <router-view />
</template>
