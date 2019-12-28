<template>
  <div id="app">
    <div class="col-sm-12">
      Valurap Control Panel
    </div>
    <div class="row">
      <div class="col-sm-3"/>
      <div class="col-sm-2">
        <div class="row">
          <div v-model="show" class="d-inline">X: {{$store.state.cur_x}}</div>
        </div>
        <div class="row">
          <div v-model="show" class="d-inline">Y: {{$store.state.cur_y}}</div>
        </div>
        <div class="row">
          <div v-model="show" class="d-inline">Z: {{$store.state.cur_z}}</div>
        </div>
      </div>
      <div class="col-sm-3"/>
      <div class="col-sm-3">
        <div class="row">
          <div class="col-sm-12">
            <b-button class="my-1" @click="sendCommand('up')">^</b-button>
          </div>
        </div>
        <div class="row">
          <div class="col-sm-12">
            <b-button class="my-1 mx-4" @click="sendCommand('left')">&lt;</b-button>
            <b-button class="my-1 mx-4" @click="sendCommand('right')">&gt;</b-button>
          </div>
        </div>
        <div class="row">
          <div class="col-sm-12">
            <b-button class="my-1" @click="sendCommand('down')">v</b-button>
          </div>
        </div>
      </div>
      <div class="col-sm-1"/>
    </div>
  </div>
</template>

<script>

  export default {
    name: 'app',
    components: {},
    methods: {
      sendCommand: function (cmd) {
        this.$socket.emit('send_command', cmd)
      },
    }
  }
</script>

<style>
  #app {
    font-family: 'Avenir', Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
    margin-top: 60px;
  }
</style>
