<template>
  <b-button
    :class="btn_class"
    @click="do_evt('click')"
    @touchstart.prevent="do_evt('touch')"
    @touchend.prevent="do_evt('touchend')"
    @touchcancel.prevent="do_evt('touchcancel')"
    @mousedown.prevent="do_evt('mousedown')"
    @mouseup.prevent="do_evt('mouseup')"
    @mouseleave.prevent="do_evt('mouseleave')"
  >
    {{ comment }}
  </b-button>
</template>

<script>
  export default {
    name: 'Button',
    data() {
      return {
        state: 'default',
        timeout: null,
        btn_class: this.$props.def_class,
      }
    },
    props: {
      comment: String,
      cmd: String,
      def_class: String
    },
    methods: {
      do_evt: function (evt) {
        if (this.state === 'default') {
          if (evt === "mouseleave" || evt === "click") {
            // nothing
          } else if (evt === 'mousedown') {
            this.state = 'mdown';
            this.btn_class = "btn-info";

            if (this.timeout)
              clearTimeout(this.timeout);

            this.timeout = setTimeout(() => this.do_evt("timeout"), 300);
          } else if (evt === 'touch') {
            this.state = 'touch';
            if (this.timeout)
              clearTimeout(this.timeout);

            this.btn_class = "btn-info";
            this.timeout = setTimeout(() => this.do_evt("timeout"), 300);
          } else {
            console.log("Unexpected event: " + evt + "@" + this.state);
          }
        } else if (this.state === 'mdown') {
          if (evt === "timeout") {
            this.state = 'active_mouse';
            this.timeout = null;
            this.sendCommand('start-');
            this.btn_class = "btn-success";
          } else if (evt === "mouseup" || evt === "mouseleave") {
            this.state = 'default';
            this.btn_class = this.$props.def_class;
            this.sendCommand('');
            if (this.timeout)
              clearTimeout(this.timeout);
          } else
            console.log("Unexpected event: " + evt + "@" + this.state);
        } else if (this.state === 'active_mouse') {
          if (evt === "mouseup" || evt === "mouseleave") {
            this.state = 'default';
            this.sendCommand('stop-');
            this.btn_class = this.$props.def_class;
          } else
            console.log("Unexpected event: " + evt + "@" + this.state);
        } else if (this.state === 'touch') {
          if (evt === "timeout") {
            this.state = 'active_touch';
            this.timeout = null;
            this.btn_class = "btn-success";
            this.sendCommand('start-');
          } else if (evt === "touchend" || evt === "touchcancel") {
            this.state = 'default';
            this.btn_class = this.$props.def_class;
            this.sendCommand('');
            if (this.timeout)
              clearTimeout(this.timeout);
          } else
            console.log("Unexpected event: " + evt + "@" + this.state);
        } else if (this.state === 'active_touch') {
          if (evt === "touchend" || evt === "touchcancel") {
            this.state = 'default';
            this.sendCommand('stop-');
            this.btn_class = this.$props.def_class;
          } else
            console.log("Unexpected event: " + evt + "@" + this.state);
        }
      },
      sendCommand: function (cmd) {
        this.$socket.emit('send_command', cmd + this.$props.cmd)
      },
    }
  }
</script>


