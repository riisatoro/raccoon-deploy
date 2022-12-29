import {defineStore} from "pinia";

export const useUserStore = defineStore("user", {
  state: () => ({isAuthenticated: false}),
  getters: {
    getIsAuthenticated: (state) => state.isAuthenticated,
  },
  actions: {
    setIsAuthenticated: (payload) => this.isAuthenticated = payload,
  }
});
