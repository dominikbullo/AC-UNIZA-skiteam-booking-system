import Vue from 'vue'
import { AclInstaller, AclCreate, AclRule } from 'vue-acl'
import router from '@/router'

// https://www.npmjs.com/package/vue-acl

Vue.use(AclInstaller)
// TODO change
let initialRole = 'admin'

// TODO change
const userInfo = JSON.parse(localStorage.getItem('userInfo'))
if (userInfo && userInfo.userRole) initialRole = userInfo.userRole

export default new AclCreate({
  initial: initialRole,
  notfound: '/pages/not-authorized',
  router,
  acceptLocalRules: true,
  globalRules: {
    admin: new AclRule('admin').generate(),
    editor: new AclRule('editor').or('admin').generate(),
    coach: new AclRule('coach').or('admin').generate(),
    parent: new AclRule('parent').or('admin').generate(),
    child: new AclRule('child').or('admin').generate()
  }
})
