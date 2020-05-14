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
  SET_CATEGORIES (state, categories) {
    state.eventConfig.categories = categories
  },
  SET_LOCATIONS (state, locations) {
    state.eventConfig.locations = locations
  },
  SET_ORGANIZERS (state, locations) {
    state.eventConfig.organizers = locations
  },
  SET_EVENT_CHOICES (state, choices) {
    state.eventConfig.choices = choices
  },
  UPDATE_EVENT (state, event) {
    const eventIndex = state.events.findIndex((e) => e.id === event.id)
    if (eventIndex === -1) {
      console.log('[MUT] Event push')
      state.events.push(event)
    } else {
      console.log('[MUT] Event update')
      Object.assign(state.events[eventIndex], event)
    }
  },
  DELETE_EVENT (state, event) {
    const eventIndex = state.events.findIndex((e) => e.id === event.id)
    state.events.splice(eventIndex, 1)
  }
}
