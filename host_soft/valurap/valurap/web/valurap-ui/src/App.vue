<template>
  <div id="app">
    <div class="col-sm-12">
      Valurap Control Panel
    </div>
    <div class="row">
      <div class="col-sm-1"/>
      <div class="col-sm-3">
        <div class="row">
          <div class="d-inline">X: {{$store.state.cur_x}}</div>
        </div>
        <div class="row">
          <div class="d-inline">Y: {{$store.state.cur_y}}</div>
        </div>
        <div class="row">
          <div class="d-inline">Z: {{$store.state.cur_z}}</div>
        </div>
      </div>
      <div class="col-sm-4"/>
      <div class="my-button-box">
        <div class="row">
          <div class="col-sm-4"/>
          <div class="col-sm-4 p-2">
            <Button cmd="up" class="py-4 btn-block" comment="^"/>
          </div>
          <div class="col-sm-4"/>
        </div>
        <div class="row">
          <div class="col-sm-4 p-2">
            <Button cmd="left" class="py-4 btn-block" comment="&lt;"/>
          </div>
          <div class="col-sm-4"/>
          <div class="col-sm-4 p-2">
            <Button cmd="right" class="py-4 btn-block" comment="&gt;"/>
          </div>
        </div>
        <div class="row">
          <div class="col-sm-4"/>
          <div class="col-sm-4 p-2">
            <Button cmd="down" class="py-4 btn-block" comment="v"/>
          </div>
          <div class="col-sm-4"/>
        </div>
      </div>
      <div class="col-sm-1"/>
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
  .my-button-box {
     min-width: 20em;
     max-width: 20em;
    min-height: 30em;
    max-height: 30em;
  }
</style>
