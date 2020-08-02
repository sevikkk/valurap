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
      console.log("socket connect");
    },
    SOCKET_error(message) {
      console.log("socket error");
    },
    SOCKET_disconnect(message) {
      console.log("socket disconnect");
    },
    SOCKET_connect_error(message) {
      console.log("socket connect_error");
    },
    SOCKET_connect_timeout(message) {
      console.log("socket connect_timeout");
    },
    SOCKET_reconnect_error(message) {
      console.log("socket reconnect_error");
    },
    SOCKET_reconnect_failed(message) {
      console.log("socket reconnect_failed");
    },
    SOCKET_ping(message) {
      console.log("socket ping");
    },
    SOCKET_pong(message) {
      console.log("socket pong");
    },
  },
  modules: {
  }
})
