<template>
  <div>
    <H1>this is event list</H1>
    <p> {{events}}</p>
  </div>
</template>

<script>

export default {
  computed: {
    events () {
      const members = this.$store.state.calendar.events
      console.log('events', members)
      return members
    }
  },
  created () {
    this.$store.dispatch('calendar/fetchEvents')
  }
}
</script>

<style>

</style>
