import axios from '@/axios.js'

export default {
  addChild ({ commit }, payload) {
    payload.profile.user_role = 'child'
    console.log(' [FAMILY STORE ACT] Add child payload', payload)

    return new Promise((resolve, reject) => {
      axios.post('/child/', { user: payload })
        .then((response) => {
          console.log('response after child added ', response)
          commit('ADD_MEMBER', Object.assign(payload, { user: response.data }))
          resolve(response)
        })
        .catch((error) => {
          reject(error)
        })
    })
  },
  fetchFamily ({ commit }, familyId) {
    console.log('[FAMILY STORE ACT] Fetching family', familyId)

    return new Promise((resolve, reject) => {
      axios.get(`/family/${familyId}/`)
        .then((response) => {
          commit('UPDATE_FAMILY', response.data)
          // TODO IDEA: set only children
          // TODO FIXME: UPDATE_FAMILY_INFO
          // commit('UPDATE_FAMILY_INFO', response.data)
          resolve(response)
        })
        .catch((error) => {
          reject(error)
        })
    })
  },
  // RES https://stackoverflow.com/questions/53501185/how-to-post-query-parameters-with-axios
  fetchUserStats ({ commit }, payload = { query: { season: 'current' } }) {
    if (!payload.query) {
      payload.query = { season: 'current' }
    }
    console.log('[FAMILY STORE ACT] payload in fetchUserStats', payload)

    if (!('username' in payload)) {
      console.error('Not found any username in payload')
      return
    }

    return new Promise((resolve, reject) => {
      axios.get(`/profile/${payload.username}/stats/`, { params: payload.query })
        .then((response) => {
          // commit('UPDATE_FAMILY_MEMBER_STATS', response.data)
          resolve(response)
        })
        .catch((error) => {
          reject(error)
        })
    })
  }
}
