import axios from '../../../axios'
import store from '../../../../store/store.js'

// Token Refresh
const isAlreadyFetchingAccessToken = false
let subscribers = []

function onAccessTokenFetched (access_token) {
  subscribers = subscribers.filter(callback => callback(access_token))
}

function addSubscriber (callback) {
  subscribers.push(callback)
}

export default {
  logout () {
    return axios.post('/rest-auth/logout/', {})
  },
  login (email, pwd) {
    return axios.post('/rest-auth/login/', {
      username: email,
      password: pwd
    })
  },
  registerUserEmail (first_name, last_name, user_role, birth_date, email, gender, password) {
    return axios.post('/rest-auth/register/', {
      email,
      first_name,
      last_name,
      password1: password,
      password2: password,
      profile: {
        user_role,
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
