export default {
  getEvent: state => (id) => state.events.find((event) => event.id === id),
  getEventParticipants: (state, getters) => (id) => getters.getEvent(id).participants,
  getEventResponses: (state, getters) => (id) => getters.getEvent(id).responses,
  getEventMergedResponses: (state, getters) => (id) => getters.getEvent(id).responses_merged,

  getType: state => (id) => state.eventConfig.types.find((e) => e.id === id),
  needSkis: (state, getters) => (id) => getters.getType(id)['need_skis'],
  isSkiTraining: (state, getters) => (id) => {
    const type = getters.getType(id)
    return type['need_skis'] && type['type'] === 'TRAINING'
  },
  isSkiRace: (state, getters) => (id) => {
    const type = getters.getType(id)
    return type['need_skis'] && type['type'] === 'RACE'
  },
  getResourceType: (state, getters) => (id) => {
    console.log('getting gesourcetype')
    if (getters.isSkiTraining(id)) return 'SkiTraining'
    if (getters.isSkiRace(id)) return 'SkiRace'
    return 'Event'
  },
  getEventsForCal: state => {
    function getData (obj) {
      return {
        id: obj.id,
        start: obj.start,
        allDay: obj.all_day,
        end: obj.end,
        title: obj.type.displayName,
        color: obj.type.color,
        textColor: obj.type.text_color,
        canceled: obj.canceled
      }
    }

    const ret = []
    state.events.forEach((element) => {
      ret.push(getData(element))
    })
    return ret
  }
}
