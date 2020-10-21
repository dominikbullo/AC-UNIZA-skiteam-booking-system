/* =========================================================================================
  File Name: moduleAuthActions.js
  Description: Auth Module Actions
  ----------------------------------------------------------------------------------------
  Item Name: Vuexy - Vuejs, HTML & Laravel Admin Dashboard Template
  Author: Pixinvent
  Author URL: http://www.themeforest.net/user/pixinvent
========================================================================================== */

import drf from '../../http/requests/auth/drf'

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

          // Navigate User to homepage
          // router.push(router.currentRoute.query.to || '/')

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
  }
}
