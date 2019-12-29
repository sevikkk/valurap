import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    cur_x: -1000000,
    cur_y: -1000000,
    cur_z: -1000000
  },
  mutations: {
    SOCKET_cur_state(state, message) {
      console.log("bubu");
      state.cur_x = message.X;
      state.cur_y = message.Y;
      state.cur_z = message.Z;
      console.log(`New state: ${message.X} ${message.Y} ${message.Z}`)
    }
  },
  actions: {
    SOCKET_MESSAGE(message) {
      console.log("bubu1");
    },
    SOCKET_connect(message) {
      console.log("bubu2");
    },
  },
  modules: {
  }
})
