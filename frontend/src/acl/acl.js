import Vue from 'vue'
import { AclInstaller, AclCreate, AclRule } from 'vue-acl'
import router from '@/router'

// https://www.npmjs.com/package/vue-acl

Vue.use(AclInstaller)
let initialRole = 'public'

const userInfo = JSON.parse(localStorage.getItem('userInfo'))
if (userInfo && userInfo.userRole) initialRole = userInfo.userRole

export default new AclCreate({
  initial: initialRole,
  notfound: {
    path: '/pages/not-authorized',
    forwardQueryParams: true
  },
  router,
  acceptLocalRules: true,
  globalRules: {
    isAdmin: new AclRule('admin').generate(),

    isCoach: new AclRule('coach').or('admin').generate(),
    isParent: new AclRule('parent').or('coach').or('admin').generate(),
    isChild: new AclRule('child').or('parent').or('coach').or('admin').generate(),

    isLogged: new AclRule('child').or('parent').or('coach').or('admin').generate(),
    isPublic: new AclRule('public').or('child').or('parent').or('coach').or('admin').generate()
  }
  // ,
  // middleware: async acl => {
  //   // TODO change role here
  //   // this.$http.get('/rest-auth/user/')
  //   //   .then((response) => {
  //   //     this.$acl.change(response.user.profile.userRole)
  //   //   })
  //   //   .catch((error) => {
  //   //     console.log(error)
  //   //     // reject(error)
  //   //   })
  //   // user, profile, userRole
  //   // console.log(this.$acl[0])
  // }
})
