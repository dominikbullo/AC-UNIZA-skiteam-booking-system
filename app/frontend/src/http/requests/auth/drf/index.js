import axios from '../../../axios/index.js'
import store from '../../../../store/store.js'

// Token Refresh
let isAlreadyFetchingAccessToken = false
let subscribers = []

function onAccessTokenFetched (access_token) {
  subscribers = subscribers.filter(callback => callback(access_token))
}

function addSubscriber (callback) {
  subscribers.push(callback)
}

export default {
  init () {
    axios.interceptors.response.use(function (response) {
      return response
    //  TODO if error ? then login again probbably
    }, function (error) {
      // const { config, response: { status } } = error
      const { config, response } = error
      const originalRequest = config

      // if (status === 401) {
      if (response && response.status === 401) {
        if (!isAlreadyFetchingAccessToken) {
          isAlreadyFetchingAccessToken = true
          store.dispatch('auth/fetchAccessTokenDRF').then((access_token) => {
            isAlreadyFetchingAccessToken = false
            onAccessTokenFetched(access_token)
          })
        }

        const retryOriginalRequest = new Promise((resolve) => {
          addSubscriber(access_token => {
            originalRequest.headers.Authorization = `Bearer ${access_token}`
            resolve(axios(originalRequest))
          })
        })
        return retryOriginalRequest
      }
      return Promise.reject(error)
    })
  },
  login (email, pwd) {
    return axios.post('/auth/login/', {
      email,
      password: pwd
    })
  },
  registerUserEmail (email, pwd) {
    return axios.post('/auth/register/', {
      email,
      password1: pwd,
      password2: pwd
    })
  },
  // https://laracasts.com/discuss/channels/laravel/how-to-refresh-xcsrf-token-after-logout-in-spa
  // refreshTokens () {
  //   return new Promise((resolve, reject) => {
  //     axios.get('/refreshtokens')
  //       .then(response => {
  //         axios.defaults.headers.common['X-CSRF-TOKEN'] = response.data.csrfToken
  //         resolve(response)
  //       })
  //       .catch(error => {
  //         reject(error)
  //       })
  //   })
  // },
  registerUserUsername (username, email, pwd) {
    return axios.post('/auth/register/', {
      username,
      password1: pwd,
      password2: pwd
    })
  }
}
