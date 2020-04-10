/* =========================================================================================
  File Name: moduleAuthActions.js
  Description: Auth Module Actions
  ----------------------------------------------------------------------------------------
  Item Name: Vuexy - Vuejs, HTML & Laravel Admin Dashboard Template
  Author: Pixinvent
  Author URL: http://www.themeforest.net/user/pixinvent
========================================================================================== */

import drf from '../../http/requests/auth/drf'

import router from '@/router'
import acl from 'vue-acl'

export default {
  updateUsername ({ commit }, payload) {
    payload.user.updateProfile({
      displayName: payload.displayName
    }).then(() => {
      // If username update is success
      // update in localstorage
      const newUserData = Object.assign({}, payload.user.providerData[0])
      newUserData.displayName = payload.displayName
      commit('UPDATE_USER_INFO', newUserData, { root: true })

      // If reload is required to get fresh data after update
      // Reload current page
      if (payload.isReloadRequired) {
        router.push(router.currentRoute.query.to || '/')
      }
    }).catch((err) => {
      payload.notify({
        time: 8800,
        title: 'Error',
        text: err.message,
        iconPack: 'feather',
        icon: 'icon-alert-circle',
        color: 'danger'
      })
    })
  },
  // logout: ({ commit }, payload) => {
  //   return new Promise((resolve, reject) => {
  //     // CRSF token
  //     // https://laracasts.com/discuss/channels/laravel/how-to-refresh-xcsrf-token-after-logout-in-spa
  //     // https://docs.djangoproject.com/en/3.0/ref/csrf/
  //
  //     // remove the axios default header
  //
  //     drf.logout().then(() => {
  //       console.log('logged out')
  //
  //       if (localStorage.getItem('userInfo')) {
  //         localStorage.removeItem('userInfo')
  //       }
  //       delete this.$http.defaults.headers.common['Authorization']
  //     })
  //
  //     if (localStorage.getItem('accessToken')) {
  //       localStorage.removeItem('accessToken')
  //     }
  //     resolve()
  //   })
  // },
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

          // Set bearer token in axios
          commit('SET_BEARER', response.data.key)

          // TODO display name add to response
          // TODO update family!
          // this.$store.dispatch('family/fetchFamily', response.data.user.profile.family_id)

          // Navigate User to homepage
          router.push(router.currentRoute.query.to || '/')

          resolve(response)
        } else {
          reject({ message: 'Wrong Email or Password' })
        }
      }).catch(() => {
        reject({ message: 'Wrong Email or Password' })
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
          // TODO response.token
          localStorage.setItem('accessToken', response.data.key)

          commit('UPDATE_USER_INFO', response.data.user, { root: true })

          // Redirect User
          router.push(router.currentRoute.query.to || '/')

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
