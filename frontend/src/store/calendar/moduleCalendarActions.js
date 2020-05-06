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
  fetchEvents ({ commit }, payload = { query: { season: 'current' } }) {
    console.log('payload fetch events', payload)

    return new Promise((resolve, reject) => {
      axios.get('/event/', {
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
  fetchEvent (context, eventId) {
    console.log('payload fetch event', eventId)
    return new Promise((resolve, reject) => {
      axios.get(`/event/${eventId}/`)
        .then((response) => {
          resolve(response)
        })
        .catch((error) => {
          reject(error)
        })
    })
  },
  changeEventMembers ({ commit }, payload) {
    const apiPayload = {
      'add': payload.selected.filter(x => !payload.onEvent.includes(x)),
      'delete': payload.onEvent.filter(x => !payload.selected.includes(x))
    }
    console.log('delete', apiPayload)

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
  }
}
