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
  SET_SKIS_TYPES (state, skis) {
    state.eventConfig.skis = skis
  },
  SET_EVENT_TYPES (state, types) {
    state.eventConfig.types = types
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
  ADD_EVENT_ACCOMMODATION (state, payload) {
    console.log('ADD_EVENT_ACCOMMODATION', payload)
    state.events.find(x => x.id === payload.eventID).accommodation.push(payload.acc)
    console.log('event', state.events.find(x => x.id === payload.eventID))
    console.log('state', state.events)
  },
  UPDATE_EVENT_ACCOMMODATION (state, payload) {
    // console.log('state.events', state.events)
    const event = state.events.find(x => x.id === payload.eventID)
    const event_acc = event.accommodation.find(x => x.id === payload.acc.id)
    Object.assign(event_acc, payload.acc)
  },
  DELETE_EVENT (state, event) {
    const eventIndex = state.events.findIndex((e) => e.id === event.id)
    state.events.splice(eventIndex, 1)
  }
}
