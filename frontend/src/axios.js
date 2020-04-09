// axios
import axios from 'axios'

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
}, function (error) {
  console.error('[AXIOS] Response Interceptors Error', error)

  // FIXME: If you ever get an unauthorized, logout the user
  // RES: https://blog.sqreen.com/authentication-best-practices-vue/
  // return new Promise(function (resolve, reject) {
  //   if (err.status === 401 && err.config && !err.config.__isRetryRequest) {
  //     // if you ever get an unauthorized, logout the user
  //     this.$store.dispatch(AUTH_LOGOUT)
  //     // you can also redirect to /login if needed !
  //   }
  //   throw err
  // })
  return Promise.reject(error)
})

//https://stackoverflow.com/questions/54836387/getting-django-vue-cors-and-csrf-working-with-a-real-world-example
instance.defaults.xsrfHeaderName = 'X-CSRFToken'
instance.defaults.xsrfCookieName = 'csrftoken'

export default instance
