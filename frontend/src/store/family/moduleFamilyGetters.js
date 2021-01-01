export default {
  familyChildren: state => {
    return state.members.filter(member => member.user.profile.user_role === 'child')
  },
  usernames: state => (members = state.members) => {
    const userNames = []
    members.forEach((element) => {
      userNames.unshift(element['user']['username'])
    })
    return userNames
  },
  fullName: state => (members = state.members) => {
    const userNames = []
    members.forEach((element) => {
      userNames.unshift(element['user']['profile']['full_name'])
    })
    return userNames
  },
  fullNameAndUsername: state => (members = state.members) => {
    const ret = []
    members.forEach((element) => {
      ret.unshift(element['user']['profile']['full_name'])
    })
    return ret
  }
}
