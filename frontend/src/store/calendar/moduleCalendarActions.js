/*=========================================================================================
  File Name: moduleCalendarActions.js
  Description: Calendar Module Actions
  ----------------------------------------------------------------------------------------
  Item Name: Vuexy - Vuejs, HTML & Laravel Admin Dashboard Template
  Author: Pixinvent
  Author URL: http://www.themeforest.net/user/pixinvent
==========================================================================================*/

import axios from '@/axios.js'

export default {
  addEvent ({ commit }, event) {
    return new Promise((resolve, reject) => {
      axios.post('/season/events/', {event})
        .then((response) => {
          commit('ADD_EVENT', Object.assign(event, {id: response.data.id}))
          resolve(response)
        })
        .catch((error) => { reject(error) })
    })
  },
  // events: [
  //   {
  //     id: 1,
  //     title: 'My Event',
  //     startDate: new Date(new Date() - 1000 * 60 * 60 * 24 * 3),
  //     endDate: new Date(new Date() - 1000 * 60 * 60 * 24 * 2),
  //     url: '',
  //     classes: 'event-success',
  //     label: 'business'
  //   }
  // ],
  fetchEvents ({ commit }) {
    return new Promise((resolve, reject) => {
      axios.get('season/events/')
        .then((response) => {
          commit('SET_EVENTS', response.data.results)
          resolve(response)
        })
        .catch((error) => { reject(error) })
    })
  },
  // labels: [
  //   {
  //     text: 'Business',
  //     value : 'business',
  //     color: 'success'
  //   },
  //   {
  //     text: 'Work',
  //     value: 'work',
  //     color: 'warning'
  //   },
  //   {
  //     text: 'Personal',
  //     value: 'personal',
  //     color: 'danger'
  //   }
  // ]
  fetchEventLabels ({ commit }) {
    return new Promise((resolve, reject) => {
      axios.get('/event/labels/')
        .then((response) => {
          commit('SET_LABELS', response.data.results)
          resolve(response)
        })
        .catch((error) => { reject(error) })
    })
  },
  editEvent ({ commit }, event) {
    return new Promise((resolve, reject) => {
      axios.post(`/api/apps/calendar/event/${event.id}`, {event})
        .then((response) => {

          // Convert Date String to Date Object
          const event = response.data
          event.startDate = new Date(event.startDate)
          event.endDate = new Date(event.endDate)

          commit('UPDATE_EVENT', event)
          resolve(response)
        })
        .catch((error) => { reject(error) })
    })
  },
  removeEvent ({ commit }, eventId) {
    return new Promise((resolve, reject) => {
      axios.delete(`/api/apps/calendar/event/${eventId}`)
        .then((response) => {
          commit('REMOVE_EVENT', response.data)
          resolve(response)
        })
        .catch((error) => { reject(error) })
    })
  },
  eventDragged ({ commit }, payload) {
    return new Promise((resolve, reject) => {
      axios.post(`/api/apps/calendar/event/dragged/${payload.event.id}`, {payload})
        .then((response) => {

          // Convert Date String to Date Object
          const event = response.data
          event.startDate = new Date(event.startDate)
          event.endDate = new Date(event.endDate)

          commit('UPDATE_EVENT', event)
          resolve(response)
        })
        .catch((error) => { reject(error) })
    })
  }
}
