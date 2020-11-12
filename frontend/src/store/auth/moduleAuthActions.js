import drf from '../../http/requests/auth/drf'
import axios from '@/axios.js'

export default {
  loginDRF ({ commit }, payload) {
    return new Promise((resolve, reject) => {
      drf.login(payload.userDetails.email, payload.userDetails.password).then(response => {
        if (response.data.user) {
          //  FIXME: If children doesn't have email then skip verification
          // if user has verified email
          // RELEASE : User must be verified!
          // if (!response.data.user.verified_email) {
          //   return reject({message: 'User not verified!'})
          // }

          // Set accessToken
          localStorage.setItem('accessToken', response.data.key)

          // Update user details
          commit('UPDATE_USER_INFO', response.data.user, { root: true })
          // TODO or Test FIXME id missmatch Profile/User
          commit('UPDATE_USER_INFO', response.data.user.profile, { root: true })

          // Set bearer token in axios
          commit('SET_BEARER', response.data.key)

          resolve(response)
        } else {
          reject({ message: 'Wrong Email or Password' })
        }
      }).catch((err) => {
        console.log(err)
        reject(err)
      })
    })
  },
  registerUserDRF ({ commit }, payload) {
    // TODO cleaner
    // for (const property of Object.keys(payload)) {
    //
    //   if (payload[property] !== null) {
    //     // Update key in localStorage
    //     userInfo[property] = payload[property]
    //   }
    // }
    const {
      first_name,
      last_name,
      user_role,
      birth_date,
      email,
      gender,
      password,
      confirmPassword
    } = payload.userDetails

    console.log('payload', payload.userDetails)

    return new Promise((resolve, reject) => {
      // Check confirm password
      if (password !== confirmPassword) {
        reject({ message: 'Password doesn\'t match. Please try again.' })
      }

      drf.registerUserEmail(first_name, last_name, user_role, birth_date, email, gender, password)
        .then(response => {
          localStorage.setItem('accessToken', response.data.key)

          // Update user details
          commit('UPDATE_USER_INFO', response.data.user, { root: true })
          commit('UPDATE_USER_INFO', response.data.user.profile, { root: true })

          // Set bearer token in axios
          commit('SET_BEARER', response.data.key)

          resolve(response)
        }).catch(error => {
        // TODO send error messages
        // How to display serializers validation error in vue
        // https://github.com/axios/axios/issues/960
          reject(error)
        })
    })
  },
  forgotPassword (context, email) {
    return new Promise((resolve, reject) => {
      axios.post('/rest-auth/reset-password/', { email })
        .then(response => {
          resolve(response)
        })
        .catch(error => {
          if (error.response.data.email && Array.isArray(error.response.data.email)) {
            reject({ message: error.response.data.email.join() })
          }
          reject({ message: 'Some unknown think happened. Please contact administrator.' })
        })
    })
  },
  resetPassword (context, payload) {
    return new Promise((resolve, reject) => {
      axios.post('/rest-auth/reset-password/confirm/', {
        password: payload.password,
        token: payload.token
      })
        .then((response) => {
          resolve(response)
        })
        .catch((error) => {
          const error_data = error.response.data
          if (error_data.password) {
            reject({
              title: 'Something wrong with password',
              message: error_data.password.join()
            })
          }
          if (error_data.status) {
            reject({
              title: 'Token already used',
              message: 'Token was already used for resetting password'
            })
          }
        })
    })
  }
}
