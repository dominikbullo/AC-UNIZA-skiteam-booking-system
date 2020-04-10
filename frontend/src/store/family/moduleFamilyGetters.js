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
//const event = Object.values(this.calendarEvents).find(obj => {
//         return obj.id === this.childAddToEventPrompt.editedEventID
//       })
//       // console.log('event', event)
//
//       // IDEA: Check with userChildren() array
//       const myChildOnEvent = event['participants'].filter(obj => {
//         return obj.family_id === this.$store.state.AppActiveUser.profile.family_id
//       })
//       // console.log('myChildOnEvent', myChildOnEvent)
//
//       const userNames = []
//       myChildOnEvent.forEach((element) => {
//         userNames.unshift(element['username'])
//       })
