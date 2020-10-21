/* =========================================================================================
  File Name: main.js
  Description: main vue(js) file

========================================================================================== */


import Vue, { createApp, h } from 'vue'
import App from './App.vue'
import './registerServiceWorker'

// Vuesax Component Framework
import Vuesax from 'vuesax'
import 'material-icons/iconfont/material-icons.css' // Material Icons
import 'vuesax/dist/vuesax.css'

// Moment (Dates)
import moment from 'moment'

// axios
import axios from './axios.js'

// API Calls
import './http/requests'

// Theme Configurations
import '../themeConfig.js'

// Firebase
// import '@/firebase/firebaseConfig'

// ACL
import acl from './acl/acl'


// Globally Registered Components
import './globalComponents.js'


// Styles: SCSS
import './assets/scss/main.scss'


// Tailwind
import '@/assets/css/main.css'


// Vue Router
import router from './router'


// Vuex Store
import store from './store/store'


// i18n
import i18n from './i18n/i18n'


// Vuexy Admin Filters
import './filters/filters'


// Clipboard
import VueClipboard from 'vue-clipboard2'


// Tour
import VueTour from 'vue-tour'


// VeeValidate
import VeeValidate from 'vee-validate'


// Google Maps
import * as VueGoogleMaps from 'vue2-google-maps'

// Vuejs - Vue wrapper for hammerjs
import { VueHammer } from 'vue2-hammer'


// PrismJS
import 'prismjs'
import 'prismjs/themes/prism-tomorrow.css'

// Raven, Sentry
import VueRaven from 'vue-raven'

Vue.use(Vuesax)

Vue.prototype.moment = moment
Vue.prototype.$http = axios

Vue.use(VueClipboard)

Vue.use(VueTour)

require('vue-tour/dist/vue-tour.css')

Vue.use(VeeValidate)

Vue.use(VueGoogleMaps, {
  load: {
    // Add your API key here
    key: 'AIzaSyB4DDathvvwuwlwnUu7F4Sow3oU22y5T1Y',
    libraries: 'places' // This is required if you use the Auto complete plug-in
  }
})

Vue.use(VueHammer)


// Feather font icon
require('./assets/css/iconfont.css')

Vue.use(VueRaven, {
  dsn: process.env.VUE_APP_SENTRY_PUBLIC_DSN,
  disableReport: process.env.NODE_ENV === 'development'
})


createApp({
  i18n,
  acl,
  render: () => h(App)
}).use(router).use(store).mount('#app')
