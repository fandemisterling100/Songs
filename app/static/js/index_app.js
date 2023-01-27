import "bootstrap"
import "../sass/index_app.scss"

import Vue from "vue"
import App from "./App.vue"
import store from "./store/state"
import 'bootstrap-vue/dist/bootstrap-vue.css'
import { BootstrapVue } from "bootstrap-vue"
import { ValidationObserver, ValidationProvider, extend } from 'vee-validate';
import * as rules from "vee-validate/dist/rules"
import './store/utils/validations'
import $ from "jquery"

Vue.use(BootstrapVue);
Vue.component('ValidationProvider', ValidationProvider)
Vue.component('ValidationObserver', ValidationObserver)

if (document.getElementById('app') != null) {
    new Vue({
        store,
        render: h => h(App),
    }).$mount('#app')
}