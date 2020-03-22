export default {
  SET_FAMILY_MEMBERS (state, payload) {
    console.log('setting up family members:', payload)
    state.members = payload
  },
  ADD_MEMBER (state, payload) {
    console.log('ading member', payload)
    state.members.unshift(payload.user)
  },
  UPDATE_FAMILY_INFO (state, payload) {
    // Get Data localStorage
    const userInfo = JSON.parse(localStorage.getItem('familyInfo')) || state.AppActiveUser

    // TODO if exist
    // When changing permission this change to undefined
    payload.displayName = `${payload.first_name} ${payload.last_name}`

    for (const property of Object.keys(payload)) {

      if (payload[property] !== null) {
        // If some of user property is null - user default property defined in state.AppActiveUser
        state.AppActiveUser[property] = payload[property]

        // Update key in localStorage
        userInfo[property] = payload[property]
      }
    }
    // Store data in localStorage
    localStorage.setItem('userInfo', JSON.stringify(userInfo))
  }
}
