/*=========================================================================================
  File Name: moduleCalendarGetters.js
  Description: Calendar Module Getters
  ----------------------------------------------------------------------------------------
  Item Name: Vuexy - Vuejs, HTML & Laravel Admin Dashboard Template
  Author: Pixinvent
  Author URL: http://www.themeforest.net/user/pixinvent
==========================================================================================*/


export default {
  getEvent: state => (eventId) => state.events.find((event) => event.id === eventId),
  getEventsForCal: state => {
    function getData (obj) {
      return {
        id: obj.id,
        start: obj.start,
        end: obj.start,
        title: obj.type.displayName,
        color: obj.type.color,
        textColor: obj.type.text_color,
        participants: obj.participants
      }
    }

    const ret = []
    state.events.forEach((element) => {
      ret.push(getData(element))
    })
    return ret
  }
}
