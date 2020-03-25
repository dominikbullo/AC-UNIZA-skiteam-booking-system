import state from './moduleEventState.js'
import mutations from './moduleEventMutations.js'
import actions from './moduleEventActions.js'
import getters from './moduleEventGetters.js'

export default {
  namespaced: true,
  state,
  mutations,
  actions,
  getters
}

