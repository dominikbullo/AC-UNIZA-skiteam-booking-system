export default {
  getAppUsers: state => {
    return state.users
  },
  getAppUsersChildren: (state, getters) => {
    return getters.getAppUsers.filter(member => member.user_role === 'child')
  }
}
