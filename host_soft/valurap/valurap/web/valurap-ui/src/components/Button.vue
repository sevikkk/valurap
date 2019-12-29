<template>
  <b-button
            @click="sendCommand('')"
            @touchstart.prevent="sendCommand('touch-')"
            @touchend.prevent="sendCommand('touchend-')"
            @touchcancel.prevent="sendCommand('touchcancel-')"
            @mousedown="sendCommand('mousedown-')"
            @mouseup="sendCommand('mouseup-')"
            @mouseleave="sendCommand('mouseleave-')"
  >
    <div class="my-3 mx-3">
      {{ comment }}
    </div>
  </b-button>
</template>

<script>
export default {
  name: 'Button',
  props: {
    comment: String,
    cmd: String
  },
  methods: {
      sendCommand: function (cmd) {
        this.$socket.emit('send_command', cmd + this.$props.cmd)
      },
  }
}
</script>


