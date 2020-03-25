export default {
  SET_EVENTS (state, payload) {
    console.log('setting up event members:', payload)
    state.members = payload
  },
  ADD_EVENT (state, payload) {
    console.log('ading event', payload)
    state.members.unshift(payload.user)
  }
}
