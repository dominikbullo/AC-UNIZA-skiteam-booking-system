/*=========================================================================================
  File Name: moduleCalendarGetters.js
  Description: Calendar Module Getters
  ----------------------------------------------------------------------------------------
  Item Name: Vuexy - Vuejs, HTML & Laravel Admin Dashboard Template
  Author: Pixinvent
  Author URL: http://www.themeforest.net/user/pixinvent
==========================================================================================*/


export default {
  // eslint-disable-next-line eqeqeq
  getEvent: state => (eventId) => state.events.find((event) => event.id == eventId),
  // getMyChildrenFromEvent: state => (eventId) => state.events.participants.filter(obj => {
  //   return obj.family_id === this.store.state.AppActiveUser.profile.family_id
  // }),
  getEventsForCal: state => {
    function getData (obj) {
      return {
        id: obj.id,
        start: obj.start,
        end: obj.end,
        title: obj.type.displayName,
        color: obj.type.color,
        textColor: obj.type.text_color
      }
    }

    const ret = []
    state.events.forEach((element) => {
      ret.push(getData(element))
    })
    return ret
  }
}
