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
      <div class="col-sm-2"/>
      <div class="col-sm-4">
        <div class="row">
          <div class="col-sm-12">
            <Button cmd="up" class="my-3" comment="^"/>
          </div>
        </div>
        <div class="row">
          <div class="col-sm-12">
            <Button cmd="left" class="mx-5" comment="&lt;"/>
            <Button cmd="right" class="mx-5" comment="&gt;"/>
          </div>
        </div>
        <div class="row">
          <div class="col-sm-12">
            <Button cmd="down" class="my-3" comment="v"/>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  import Button from './components/Button.vue'

  export default {
    name: 'app',
    components: {
      Button
    },
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
