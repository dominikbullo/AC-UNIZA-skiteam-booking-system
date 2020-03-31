export default {
  getFamilyChildren (state) {
    console.log('childreturned', state.members.filter(member => member.user.profile.user_role === 'child'))
    return state.members.filter(member => member.user.profile.user_role === 'child')
  }
}
