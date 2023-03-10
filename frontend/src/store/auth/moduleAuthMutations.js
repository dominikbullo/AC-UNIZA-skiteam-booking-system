import axios from '../../http/axios'

export default {
  SET_BEARER (state, accessToken) {
    axios.defaults.headers.common['Authorization'] = `Token ${accessToken}`
  }
}
