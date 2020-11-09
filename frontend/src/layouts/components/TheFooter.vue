<template functional>
  <footer class="the-footer flex-wrap justify-between" :class="classes">
    <span class="md:flex hidden items-center">
            <span>
              <a href="http://acuniza.skiteam.sk/" target="_blank" rel="nofollow">AC UNIZA Ski Team</a>
              |
              <a href="http://sportagenda.sk/" target="_blank" rel="nofollow">Sport Agenda</a>
              - v{{ parent.$store.getters.appVersion }} </span>
            <feather-icon icon="HeartIcon" svgClasses="stroke-current text-danger w-6 h-6" class="ml-2"/>
        </span>
    <p>
      <span>COPYRIGHT &copy;</span>
      <span>{{ new Date().getFullYear() }} </span>
      <a href="http://dominikbullo.sk/" target="_blank" rel="nofollow">Dominik Bullo</a>
      <span class="hidden sm:inline-block">, All rights Reserved</span>
    </p>
  </footer>
</template>


<script>
export default {
  name: 'the-footer',
  props: {
    classes: {
      type: String
    }
  }
}
</script>
