export default {
  SET_FAMILY_MEMBERS (state, payload) {
    state.members = payload
  },
  ADD_MEMBER (state, child) {
    state.members.unshift(child)
  }
}
