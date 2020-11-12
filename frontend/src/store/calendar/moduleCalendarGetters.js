export default {
  getEvent: state => (id) => state.events.find((event) => event.id === id),
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
