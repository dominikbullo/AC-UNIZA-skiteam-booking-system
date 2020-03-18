/*=========================================================================================
  File Name: moduleCalendarMutations.js
  Description: Calendar Module Mutations
  ----------------------------------------------------------------------------------------
  Item Name: Vuexy - Vuejs, HTML & Laravel Admin Dashboard Template
  Author: Pixinvent
  Author URL: http://www.themeforest.net/user/pixinvent
==========================================================================================*/


export default {
  SET_TODO_SEARCH_QUERY (state, query) {
    state.todoSearchQuery = query
  },
  SET_FAMILY_MEMBERS (state, payload) {
    state.members = payload
  },
  ADD_MEMBER (state, child) {
    state.members.unshift(child)
  },
  UPDATE_CHILD (state, task) {
    const taskIndex = state.tasks.findIndex((t) => t.id === task.id)
    Object.assign(state.tasks[taskIndex], task)
  }
}
