import Vuex from 'vuex'

import auth from '@/store/modules/auth'

const store = Vuex.createStore({
  modules: {
    auth
  }
})

export default store
