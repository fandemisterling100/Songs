<template>
    <div class="d-flex justify-content-center align-items-center w-100 flex-column">
      hola
    </div>
  </template>
  <script>
  import Messages from './store/components/Messages.vue';
  import { mapState, mapActions } from 'vuex'

  export default {
    components: {
      "app-messages": Messages,
    },
    computed: {
      ...mapState({
      }),
    },
    data() {
      return {
      };
    },
    methods: {
      ...mapActions({
      }),
    },
    mounted() {
  },
  };
  </script>
