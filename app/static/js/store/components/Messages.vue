<template>
    <div class="alert-modal">
      <div class="position-relative">
        <b-alert
          v-for="(message, index) in messages"
          :key="index"
          :variant="message.type"
          show
          dismissible @dismissed="clearMessage(message.id)"
        >
          {{ message.message }}
        </b-alert>
      </div>
    </div>
  </template>
  
  <script>
  import { mapState } from 'vuex'
  
  export default {
    computed: mapState({
      messages: state => state.messages.all,
    }),
    methods: {
      clearMessage (id){
        this.$store.dispatch('messages/removeMessage', id)
      },
    }
  }
  </script>
  <style lang="scss">
  .alert-modal {
    z-index: 90001 !important;
    position: fixed;
    top: 10px;
    right: 10px;
    width: 50%;
  }
  </style>