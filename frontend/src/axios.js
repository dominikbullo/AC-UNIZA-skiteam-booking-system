// axios
import axios from 'axios'
import router from './router'

// RES
// https://stackoverflow.com/questions/51374367/axios-is-not-defined-in-vue-js-cli
// https://vuejs.org/v2/cookbook/using-axios-to-consume-apis.html
// https://github.com/axios/axios

const baseURL = '/api'

const instance = axios.create({
  baseURL,
  timeout: 10000,
  params: {} // do not remove this, its added to add params later in the config
})

// Add a request interceptor
instance.interceptors.request.use(function (config) {
  console.log('[AXIOS] Request Interceptors', config)
  return config
}, function (error) {
  console.error('[AXIOS] Request Interceptors Error', error)
  return Promise.reject(error)
})

// Add a response interceptor
instance.interceptors.response.use(function (response) {
  console.log('[AXIOS] Response Interceptors', response)
  return response
}, function (err) {
  console.error('[AXIOS] Response Interceptors Error', err)

  // RES: https://blog.sqreen.com/authentication-best-practices-vue/
  return new Promise(function (resolve, reject) {
    // TODO: refactor to action f.e (AUTH_LOGOUT)
    if (err.response.status === 401) {
      axios.post('/rest-auth/logout/').then(() => {
        delete axios.defaults.headers.common['Authorization']
      })

      // CRSF token
      // https://laracasts.com/discuss/channels/laravel/how-to-refresh-xcsrf-token-after-logout-in-spa
      if (localStorage.getItem('accessToken')) {
        localStorage.removeItem('accessToken')
      }

      // Change role on logout. Same value as initialRole of acj.js
      localStorage.removeItem('userInfo')

      // This is just for demo Purpose. If user clicks on logout -> redirect
      router.push({ name: 'page-login' }).catch(() => {})
      // you can also redirect to /login if needed !
      return
    }
    throw err
  })
})

//https://stackoverflow.com/questions/54836387/getting-django-vue-cors-and-csrf-working-with-a-real-world-example
instance.defaults.xsrfHeaderName = 'X-CSRFToken'
instance.defaults.xsrfCookieName = 'csrftoken'

export default instance
