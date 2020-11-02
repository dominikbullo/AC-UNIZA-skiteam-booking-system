/* =========================================================================================
  File Name: moduleCalendarActions.js
  Description: Calendar Module Actions
  ----------------------------------------------------------------------------------------
  Item Name: Vuexy - Vuejs, HTML & Laravel Admin Dashboard Template
  Author: Pixinvent
  Author URL: http://www.themeforest.net/user/pixinvent
========================================================================================== */

import axios from '@/axios.js'

export default {
  /**
   * Fetching events from server.
   *
   * @default fetching from current active season
   */
  fetchEvents ({ commit }, payload = { query: { season: {} } }) {
    return new Promise((resolve, reject) => {
      axios.get('/events/', {
        params: payload.query
      })
        .then((response) => {
          commit('SET_EVENTS', response.data.results)
          resolve(response)
        })
        .catch((error) => {
          reject(error)
        })
    })
  },
  fetchEvent ({ commit }, eventId) {
    console.log('payload fetch event', eventId)
    return new Promise((resolve, reject) => {
      axios.get(`/event/${eventId}/`)
        .then((response) => {
          commit('UPDATE_EVENT', response.data)
          resolve(response)
        })
        .catch((error) => {
          reject(error)
        })
    })
  },
  fetchSkisTypes ({ commit }, payload) {
    return new Promise((resolve, reject) => {
      // payload = { query: { season: {} } }
      axios.get('/skis-types/')
        .then((response) => {
          commit('SET_SKIS_TYPES', response.data.results)
          resolve(response)
        })
        .catch((error) => {
          reject(error)
        })
    })
  },
  fetchEventTypes ({ commit }, payload) {
    return new Promise((resolve, reject) => {
      // payload = { query: { season: {} } }
      axios.get('/event-types/')
        .then((response) => {
          commit('SET_EVENT_TYPES', response.data.results)
          resolve(response)
        })
        .catch((error) => {
          reject(error)
        })
    })
  },
  fetchLocations ({ commit }) {
    return new Promise((resolve, reject) => {
      axios.get('/locations/')
        .then((response) => {
          commit('SET_LOCATIONS', response.data.results)
          resolve(response)
        })
        .catch((error) => {
          reject(error)
        })
    })
  },
  fetchRaceOrganizers ({ commit }) {
    return new Promise((resolve, reject) => {
      axios.get('/race-organizer/')
        .then((response) => {
          commit('SET_ORGANIZERS', response.data.results)
          resolve(response)
        })
        .catch((error) => {
          reject(error)
        })
    })
  },
  fetchCategories ({ commit }) {
    return new Promise((resolve, reject) => {
      axios.get('/categories/')
        .then((response) => {
          commit('SET_CATEGORIES', response.data.results)
          resolve(response)
        })
        .catch((error) => {
          reject(error)
        })
    })
  },
  changeEventMembers ({ commit }, payload) {
    console.log('payload 1s', payload)
    const apiPayload = {
      'add': payload.eventAdd.filter(x => !payload.eventDelete.includes(x)),
      'delete': payload.eventDelete.filter(x => !payload.eventAdd.includes(x))
    }
    console.log('apiPayload', apiPayload)

    return new Promise((resolve, reject) => {
      axios.post(`event/${payload.eventID}/change/`, { users: apiPayload })
        .then((response) => {
          commit('UPDATE_EVENT', response.data)
          resolve(response)
        })
        .catch((error) => {
          reject(error)
        })
    })
  },
  deleteEvent ({ commit }, event) {
    console.log('event in actions', event)
    return new Promise((resolve, reject) => {
      axios.delete(`/event/${event.id}/`)
        .then((response) => {
          commit('DELETE_EVENT', event)
          resolve(response)
        })
        .catch((error) => {
          reject(error)
        })
    })
  },
  editEvent ({ commit }, event) {
    console.log('edit event in actions', event)
    return new Promise((resolve, reject) => {
      delete event['participants']
      axios.patch(`/event/${event.id}/`, event)
        .then((response) => {
          commit('UPDATE_EVENT', response.data)
          resolve(response)
        })
        .catch((error) => {
          reject(error)
        })
    })
  },
  addEvent ({ commit }, event) {
    console.log('add event in actions', event)
    return new Promise((resolve, reject) => {
      axios.post('/events/', event)
        .then((response) => {
          commit('ADD_EVENT', response.data)
          resolve(response)
        })
        .catch((error) => {
          reject(error)
        })
    })
  }
  // updateOrAddEvent ({ commit }, event) {
  //   commit('UPDATE_EVENT', event.data)
  // }
}
