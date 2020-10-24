import Vuex from 'vuex'

import users from '@/store/services/users'
import auth from '@/store/modules/auth'

const store = Vuex.createStore({
  modules: {
    users,
    auth
  }
})

export default store
