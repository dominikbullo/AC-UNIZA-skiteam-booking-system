import axios from '@/axios.js'
import moment from 'moment'

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
  changeEventMembersDirect ({ commit }, payload) {
    console.log('payload changeEventMembers', payload)
    return new Promise((resolve, reject) => {
      axios.patch(`event/${payload.id}/`, {
        participants: payload.data,
        resourcetype: 'Event'
      })
        .then((response) => {
          commit('UPDATE_EVENT', response.data)
          resolve(response)
        })
        .catch((error) => {
          reject(error)
        })
    })
  },
  addEventResponse ({ commit }, payload) {
    console.log('payload changeEventMembers', payload)
    return new Promise((resolve, reject) => {
      axios.post(`event/${payload.eventID}/response/`, payload.data)
        .then((response) => {
          commit('UPDATE_EVENT_RESPONSE', {
            eventID: payload.eventID,
            data: response.data
          })
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
      // FIXME: Better formatting
      console.log(moment(event.start, 'YYYY-DD-MM', true).isValid())
      //true
      event.start = moment(event.start).toISOString()
      event.end = moment(event.end).toISOString()
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
    return new Promise((resolve, reject) => {
      event.start = moment(event.start).toISOString()
      event.end = moment(event.end).toISOString()
      axios.post('/events/', event)
        .then((response) => {
          commit('ADD_EVENT', response.data)
          resolve(response)
        })
        .catch((error) => {
          reject(error)
        })
    })
  },
  createAccommodation ({
    commit,
    dispatch
  }, obj) {
    console.log('creating acco', obj)
    const eventID = obj.eventID
    delete obj.eventID

    return new Promise((resolve, reject) => {
      axios.post('/accommodation/', obj)
        .then((response) => {
          dispatch('addAccommodationToEvent', {
            eventID,
            accommodation: response.data
          })
          resolve(response)
        })
        .catch((error) => {
          reject(error)
        })
    })
  },
  updateAccommodation ({ commit }, obj) {
    console.log('updateAccommodation', obj)
    const eventID = obj.eventID
    delete obj.eventID

    return new Promise((resolve, reject) => {
      axios.patch(`/accommodation/${obj.id}`, obj)
        .then((response) => {
          console.log('res update', response)
          commit('UPDATE_EVENT_ACCOMMODATION', {
            eventID: parseInt(eventID),
            acc: response.data
          })
          resolve(response)
        })
        .catch((error) => {
          reject(error)
        })
    })
  },
  deleteAccommodation ({ commit }, id) {
    return new Promise((resolve, reject) => {
      axios.delete(`/accommodation/${id}/`)
        .then((response) => {
          resolve(response)
        })
        .catch((error) => {
          reject(error)
        })
    })
  },
  addAccommodationToEvent ({ commit }, obj) {
    console.log('addAccommodationToEvent obj', obj)

    return new Promise((resolve, reject) => {
      axios.post(`/event/${obj.eventID}/accommodation`, {
        accommodation: [obj.accommodation.id]
      })
        .then((response) => {
          commit('UPDATE_EVENT', response.data)
          resolve(response)
        })
        .catch((error) => {
          reject(error)
        })
    })
  },
  createMergedArrayFromResponsesAndUsers ({ commit }, eventID) {
    /*
     Creating merged array from responses and users to display if user fill
     response, if fill yes or no, or display blank
     1. Get all users (children)
     2. Get responses from event
     3. Add users which does not have response with going=null
     */

    const merged = []
    const eventResponses = this.getters['calendar/getEventResponses'](eventID)
    // console.log('eventResponses', eventResponses)
    const eventParticipants = this.getters['calendar/getEventParticipants'](eventID)
    // console.log('eventResponses', eventParticipants)

    this.dispatch('userManagement/fetchUsers').then(() => {
      const users = this.getters['userManagement/getAppUsers']

      for (const user of Object.values(users)) {
        const foundResponse = Object.values(eventResponses).find(x => x.user_to_event.id === user.id)
        const foundParticipants = Object.values(eventParticipants).find(x => x.id === user.id)
        // TODO: maybe iterate only responses but, if you want to add user as admin, create response object, not direct rewrite

        let going = null
        // if foundResponse
        if (foundResponse && foundResponse.hasOwnProperty('going')) {
          going = foundResponse.going
        }
        // FIXME: Pozor na to, ??e user m????e by?? pridan?? napr??klad aj adminom napriamo, to znamen??, ??e tie?? by mal ma?? going true
        // if (foundParticipants) {
        //   going = true
        // }

        const tmp = {
          going,
          'user_to_event': user
        }
        merged.push(tmp)
      }
      // console.log('***********merged**********', merged)
      commit('UPDATE_EVENT_RESPONSES', {
        eventID,
        merged
      })
    })
  }
}
