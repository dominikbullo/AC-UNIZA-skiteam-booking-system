<template>
  <div class="the-navbar__user-meta flex items-center" v-if="activeUserInfo.displayName">

    <div class="text-right leading-tight hidden sm:block">
      <p class="font-semibold">{{ activeUserInfo.displayName }}</p>
      <small>{{ activeUserInfo.userRole }}</small>
    </div>

    <vs-dropdown vs-custom-content vs-trigger-click class="cursor-pointer">

      <div class="con-img ml-3">
        <img v-if="activeUserInfo.photoURL" key="onlineImg" :src="activeUserInfo.photoURL" alt="user-img" width="40"
             height="40" class="rounded-full shadow-md cursor-pointer block"/>
      </div>

      <vs-dropdown-menu class="vx-navbar-dropdown">
        <ul style="min-width: 9rem">

          <li
            class="flex py-2 px-4 cursor-pointer hover:bg-primary hover:text-white"
            @click="$router.push('/pages/user-settings').catch(() => {})">
            <feather-icon icon="UserIcon" svgClasses="w-4 h-4"/>
            <span class="ml-2">{{ $t('Account') }}</span>
          </li>

          <li
            class="flex py-2 px-4 cursor-pointer hover:bg-primary hover:text-white"
            @click="$router.push('/apps/family/members').catch(() => {})">
            <feather-icon icon="UsersIcon" svgClasses="w-4 h-4"/>
            <span class="ml-2">{{ $t('Family') }}</span>
          </li>

          <li v-if="this.$store.state.AppActiveUser.userRole === 'child'"
              class="flex py-2 px-4 cursor-pointer hover:bg-primary hover:text-white"
              @click="$router.push('/apps/user/stats').catch(() => {})">
            <feather-icon icon="PieChartIcon" svgClasses="w-4 h-4"/>
            <span class="ml-2">{{ $t('My stats') }}</span>
          </li>

          <vs-divider class="m-1"/>

          <li
            class="flex py-2 px-4 cursor-pointer hover:bg-primary hover:text-white"
            @click="logout">
            <feather-icon icon="LogOutIcon" svgClasses="w-4 h-4"/>
            <span class="ml-2">{{ $t('Logout') }}</span>
          </li>
        </ul>
      </vs-dropdown-menu>
    </vs-dropdown>
  </div>
</template>

<script>

export default {
  data () {
    return {}
  },
  computed: {
    activeUserInfo () {
      return this.$store.state.AppActiveUser
    }
  },
  methods: {
    logout () {
      // IDEA:
      //  this.$store.dispatch('auth/logout')
      // this.$router.push('/login').catch(() => {})

      // https://docs.djangoproject.com/en/3.0/ref/csrf/
      this.$http.post('/rest-auth/logout/').then(() => {
        // delete this.$http.defaults.headers.common['X-CSRFToken']
        delete this.$http.defaults.headers.common['Authorization']
      })

      // CRSF token
      // https://laracasts.com/discuss/channels/laravel/how-to-refresh-xcsrf-token-after-logout-in-spa
      if (localStorage.getItem('accessToken')) {
        localStorage.removeItem('accessToken')
      }

      // Change role on logout. Same value as initialRole of acj.js
      localStorage.removeItem('userInfo')

      // This is just for demo Purpose. If user clicks on logout -> redirect
      this.$router.push('/login').catch(() => {
      })
    }
  }
}
</script>
