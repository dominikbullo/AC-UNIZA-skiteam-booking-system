/*=========================================================================================
  File Name: moduleCalendarMutations.js
  Description: Calendar Module Mutations
  ----------------------------------------------------------------------------------------
  Item Name: Vuexy - Vuejs, HTML & Laravel Admin Dashboard Template
  Author: Pixinvent
  Author URL: http://www.themeforest.net/user/pixinvent
==========================================================================================*/


export default {
  ADD_EVENT (state, event) {
    state.events.push(event)
  },
  SET_EVENTS (state, events) {
    state.events = events
  },
  UPDATE_EVENT (state, event) {
    const eventIndex = state.events.findIndex((e) => e.id === event.id)
    if (eventIndex === -1) {
      state.events.push(event)
    } else {
      Object.assign(state.events[eventIndex], event)
    }
  },
  DELETE_EVENT (state, event) {
    const eventIndex = state.events.findIndex((e) => e.id === event.id)
    state.events.splice(eventIndex, 1)
  }
}
