export default {
  SET_FAMILY_MEMBERS (state, members) {
    // console.log('[FAMILY STORE MUT] setting up family members:', members)
    state.members = members
  },
  ADD_FAMILY_MEMBERS (state, payload) {
    // console.log('[FAMILY STORE MUT] adding family members:', payload)
    state.members.concat(payload)
  },
  UPDATE_FAMILY (state, familyData) {
    // console.log('[FAMILY STORE MUT] Updating family with data', familyData)
    Object.assign(state, familyData)
  },
  ADD_MEMBER (state, payload) {
    // console.log('[FAMILY STORE MUT] adding member', payload)
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
