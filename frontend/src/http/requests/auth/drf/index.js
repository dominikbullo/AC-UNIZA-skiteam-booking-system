import axios from '../../../axios'
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
    // TODO get token
    // FIXME get token
    axios.interceptors.response.use(function (response) {
      return response
      //  TODO if error ? then login again probbably
    }, function (error) {
      // const { config, response: { status } } = error
      const {config, response} = error
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
  logout () {
    return axios.post('/rest-auth/logout/', {})
  },
  login (email, pwd) {
    return axios.post('/rest-auth/login/', {
      username: email,
      password: pwd
    })
  },
  registerUserEmail (first_name, last_name, birth_date, email, gender, pwd) {
    return axios.post('/rest-auth/register/', {
      email,
      first_name,
      last_name,
      password1: pwd,
      password2: pwd,
      profile: {
        birth_date,
        gender
      }

    })
  },
  registerUserUsername (username, email, pwd) {
    return axios.post('/rest-auth/register/', {
      username,
      password1: pwd,
      password2: pwd
    })
  }
}
