// axios
import axios from 'axios'
import Qs from 'qs'

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
  console.log('Request Interceptors', config)
  return config
}, function (error) {
  console.error('Request Interceptors Error', error)
  return Promise.reject(error)
})

// Add a response interceptor
instance.interceptors.response.use(function (response) {
  console.log('Response Interceptors', response)
  return response
}, function (error) {
  console.error('Response Interceptors Error', error)
  return Promise.reject(error)
})

//https://stackoverflow.com/questions/54836387/getting-django-vue-cors-and-csrf-working-with-a-real-world-example
instance.defaults.xsrfHeaderName = 'X-CSRFToken'
instance.defaults.xsrfCookieName = 'csrftoken'

export default instance
