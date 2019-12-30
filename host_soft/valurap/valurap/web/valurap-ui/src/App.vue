<template>
  <div id="app">
    <h1 class="col-sm-12 mt-4" @click="openFullScreen">
      Valurap Control Panel
    </h1>
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
      <div class="col-sm-2"/>
      <div class="my-button-box">
        <div class="row">
          <div class="col-sm-4"/>
          <div class="col-sm-4 p-2">
            <Button cmd="up" class="py-4 btn-block" def_class="btn-warning" comment="^"/>
          </div>
          <div class="col-sm-4"/>
        </div>
        <div class="row">
          <div class="col-sm-4 p-2">
            <Button cmd="left" class="py-4 btn-block" def_class="btn-warning" comment="&lt;"/>
          </div>
          <div class="col-sm-4"/>
          <div class="col-sm-4 p-2">
            <Button cmd="right" class="py-4 btn-block" def_class="btn-warning" comment="&gt;"/>
          </div>
        </div>
        <div class="row">
          <div class="col-sm-4"/>
          <div class="col-sm-4 p-2">
            <Button cmd="down" class="py-4 btn-block" def_class="btn-warning" comment="v"/>
          </div>
          <div class="col-sm-4"/>
        </div>
      </div>
      <div class="col-sm-1"/>
      <div class="col-sm-1">
        <div class="row mb-5 mt-2">
          <Button cmd="home" class="py-4 btn-block" def_class="btn-dark" comment="Home"/>
        </div>
        <div class="row">
          <Button cmd="abort" class="py-5 btn-block" def_class="btn-danger" comment="Abort"/>
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
      openFullScreen() {
        var elem = document.documentElement;
        if (elem.requestFullscreen) {
          elem.requestFullscreen();
        } else if (elem.mozRequestFullScreen) { /* Firefox */
          elem.mozRequestFullScreen();
        } else if (elem.webkitRequestFullscreen) { /* Chrome, Safari and Opera */
          elem.webkitRequestFullscreen();
        } else if (elem.msRequestFullscreen) { /* IE/Edge */
          elem.msRequestFullscreen();
        }
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
  }

  .my-button-box {
    min-width: 20em;
    max-width: 20em;
    min-height: 30em;
    max-height: 30em;
  }
</style>
