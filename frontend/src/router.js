/* =========================================================================================
  File Name: router.js
  Description: Routes for vue-router. Lazy loading is enabled.
  Object Strucutre:
                    path => router path
                    name => router name
                    component(lazy loading) => component to load
                    meta : {
                      rule => which user can have access (ACL)
                      breadcrumb => Add breadcrumb to specific page
                      pageTitle => Display title besides breadcrumb
                    }
========================================================================================== */

import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

const router = new Router({
  mode: 'history',
  // base: process.env.BASE_URL,
  scrollBehavior () {
    return {
      x: 0,
      y: 0
    }
  },
  routes: [
    {
      // =============================================================================
      // MAIN LAYOUT ROUTES
      // =============================================================================
      path: '',
      component: () => import('./layouts/main/Main.vue'),
      children: [
        // =============================================================================
        // Theme Routes
        // =============================================================================

        // =============================================================================
        // Dashboards
        // =============================================================================
        {
          path: '/',
          redirect: '/dashboard'
        },
        {
          path: '/dashboard',
          name: 'dashboard',
          component: () => import('./views/dashboards/MainDashboard.vue'),
          meta: {
            rule: 'isLogged'
          }
        },
        {
          path: '/dashboard/coach',
          name: 'dashboard-coach',
          component: () => import('./views/dashboards/CoachDashboard.vue'),
          meta: {
            rule: 'isCoach'
          }
        },
        {
          path: '/test/page',
          name: 'testpage',
          component: () => import('@/views/pages/testPages/TestPage.vue'),
          meta: {
            rule: 'isLogged'
          }
        },
        {
          path: '/test/stats',
          name: 'test-stats',
          component: () => import('@/views/pages/testPages/TestStats.vue'),
          meta: {
            rule: 'isLogged'
          }
        },
        {
          path: '/test/calendar',
          name: 'testcalendar',
          component: () => import('@/views/pages/testPages/TestCalendar.vue'),
          meta: {
            rule: 'isLogged'
          }
        },

        // =============================================================================
        // Application Routes
        // =============================================================================


        // User APP
        {
          path: '/apps/user/user-list',
          name: 'app-user-list',
          component: () => import('@/views/apps/user/user-list/UserList.vue'),
          meta: {
            breadcrumb: [
              {
                title: 'Home',
                url: '/'
              },
              { title: 'User' },
              {
                title: 'List',
                active: true
              }
            ],
            pageTitle: 'User List',
            rule: 'isParent'
          }
        },
        {
          path: '/apps/user/:userId/view',
          name: 'app-user-view',
          component: () => import('@/views/apps/user/UserView.vue'),
          meta: {
            breadcrumb: [
              {
                title: 'Home',
                url: '/'
              },
              { title: 'User' },
              {
                title: 'View',
                active: true
              }
            ],
            pageTitle: 'User View',
            rule: 'isParent'
          }
        },
        {
          path: '/apps/user/:userId?/stats',
          name: 'app-user-stats',
          component: () => import('@/views/apps/user/UserStatsView.vue'),
          meta: {
            breadcrumb: [
              {
                title: 'Home',
                url: '/'
              },
              { title: 'User' },
              {
                title: 'Stats',
                active: true
              }
            ],
            pageTitle: 'User Stats',
            rule: 'isChild'
          }
        },
        {
          path: '/apps/user/user-edit/:userId',
          name: 'app-user-edit',
          component: () => import('@/views/apps/user/user-edit/UserEdit.vue'),
          meta: {
            breadcrumb: [
              {
                title: 'Home',
                url: '/'
              },
              { title: 'User' },
              {
                title: 'Edit',
                active: true
              }
            ],
            pageTitle: 'User Edit',
            rule: 'isAdmin'
          }
        },
        // Family APP
        {
          path: '/apps/family/members',
          name: 'app-family-members',
          component: () => import('@/views/apps/family/family-members/FamilyMembersList.vue'),
          meta: {
            breadcrumb: [
              {
                title: 'Home',
                url: '/'
              },
              { title: 'Family' },
              {
                title: 'Members List',
                active: true
              }
            ],
            pageTitle: 'Family Members List',
            rule: 'isParent'
          }
        },
        {
          path: '/apps/family/:familyId?/view',
          name: 'app-family-view',
          component: () => import('@/views/apps/family/FamilyView.vue'),
          meta: {
            breadcrumb: [
              {
                title: 'Home',
                url: '/'
              },
              { title: 'Family' },
              {
                title: 'View',
                active: true
              }
            ],
            pageTitle: 'Family View',
            rule: 'isChild'
          }
        },
        {
          path: '/apps/family/:familyId?/edit/',
          name: 'app-family-edit',
          component: () => import('@/views/apps/family/family-edit/FamilyEdit.vue'),
          meta: {
            breadcrumb: [
              {
                title: 'Home',
                url: '/'
              },
              { title: 'Family' },
              {
                title: 'Edit',
                active: true
              }
            ],
            pageTitle: 'Family Edit',
            rule: 'isParent'
          }
        },

        // Event APP
        {
          path: '/apps/event/list',
          name: 'app-event-list',
          component: () => import('@/views/apps/event/event-list/EventList.vue'),
          meta: {
            breadcrumb: [
              {
                title: 'Home',
                url: '/'
              },
              { title: 'Event' },
              {
                title: 'List',
                active: true
              }
            ],
            pageTitle: 'Event List',
            rule: 'isChild'
          }
        },
        {
          path: '/apps/event/:eventId/edit',
          name: 'app-event-edit',
          component: () => import('@/views/apps/event/event-edit/EventEdit.vue'),
          meta: {
            breadcrumb: [
              {
                title: 'Home',
                url: '/'
              },
              { title: 'Event' },
              {
                title: 'Edit',
                active: true
              }
            ],
            pageTitle: 'Edit Event',
            rule: 'isCoach'
          }
        },
        {
          path: '/apps/event/calendar',
          name: 'app-event-calendar',
          component: () => import('@/views/apps/event/EventCalendar.vue'),
          meta: {
            rule: 'isChild',
            no_scroll: true
          }
        },

        // =============================================================================
        // Pages Routes
        // =============================================================================
        {
          path: '/pages/profile',
          name: 'page-profile',
          component: () => import('@/views/pages/Profile.vue'),
          meta: {
            breadcrumb: [
              {
                title: 'Home',
                url: '/'
              },
              { title: 'Pages' },
              {
                title: 'Profile',
                active: true
              }
            ],
            pageTitle: 'Profile',
            rule: 'isAdmin'
          }
        },
        {
          path: '/pages/user-settings',
          name: 'page-user-settings',
          component: () => import('@/views/pages/user-settings/UserSettings.vue'),
          meta: {
            breadcrumb: [
              {
                title: 'Home',
                url: '/'
              },
              { title: 'Pages' },
              {
                title: 'User Account',
                active: true
              }
            ],
            pageTitle: 'Settings',
            rule: 'isLogged'
          }
        },
        {
          path: '/pages/faq',
          name: 'page-faq',
          component: () => import('@/views/pages/Faq.vue'),
          meta: {
            breadcrumb: [
              {
                title: 'Home',
                url: '/'
              },
              { title: 'Pages' },
              {
                title: 'FAQ',
                active: true
              }
            ],
            pageTitle: 'FAQ',
            rule: 'isPublic'
          }
        },

        // =============================================================================
        // CHARTS & MAPS
        // =============================================================================
        {
          path: '/page/statistics',
          name: 'page-statistics',
          component: () => import('@/views/pages/stats/Statistics.vue'),
          meta: {
            breadcrumb: [
              {
                title: 'Home',
                url: '/'
              },
              { title: 'Statistics' },
              {
                title: 'Apex Charts',
                active: true
              }
            ],
            pageTitle: 'Charts',
            rule: 'isChild'
          }
        },
        // TODO detail stats for coach if i have more real data
        {
          path: '/page/statistics/detail',
          name: 'page-statistics-detail',
          component: () => import('@/views/pages/stats/Statistics.vue'),
          meta: {
            breadcrumb: [
              {
                title: 'Home',
                url: '/'
              },
              { title: 'Statistics' },
              {
                title: 'Apex Charts',
                active: true
              }
            ],
            pageTitle: 'Charts',
            rule: 'isChild'
          }
        }
      ]
    },
    // =============================================================================
    // FULL PAGE LAYOUTS
    // =============================================================================
    {
      path: '',
      component: () => import('@/layouts/full-page/FullPage.vue'),
      children: [
        // =============================================================================
        // PAGES
        // ====================test=========================================================
        {
          path: '/login',
          name: 'page-login',
          component: () => import('@/views/pages/login/Login.vue'),
          meta: {
            rule: 'isPublic'
          }
        },
        {
          path: '/register',
          name: 'page-register',
          component: () => import('@/views/pages/register/Register.vue'),
          meta: {
            rule: 'isPublic'
          }
        },
        {
          path: '/forgot-password',
          name: 'page-forgot-password',
          component: () => import('@/views/pages/ForgotPassword.vue'),
          meta: {
            rule: 'isPublic'
          }
        },
        {
          path: '/reset-password/:token',
          name: 'page-reset-password',
          component: () => import('@/views/pages/ResetPassword.vue'),
          meta: {
            rule: 'isPublic'
          }
        },
        {
          path: '/pages/lock-screen',
          name: 'page-lock-screen',
          component: () => import('@/views/pages/LockScreen.vue'),
          meta: {
            rule: 'isPublic'
          }
        },
        {
          path: '/pages/comingsoon',
          name: 'page-coming-soon',
          component: () => import('@/views/pages/ComingSoon.vue'),
          meta: {
            rule: 'isPublic'
          }
        },
        {
          path: '/pages/error-404',
          name: 'page-error-404',
          component: () => import('@/views/pages/Error404.vue'),
          meta: {
            rule: 'isPublic'
          }
        },
        {
          path: '/pages/error-500',
          name: 'page-error-500',
          component: () => import('@/views/pages/Error500.vue'),
          meta: {
            rule: 'isPublic'
          }
        },
        {
          path: '/pages/not-authorized',
          name: 'page-not-authorized',
          component: () => import('@/views/pages/NotAuthorized.vue'),
          meta: {
            rule: 'isPublic'
          }
        },
        {
          path: '/pages/maintenance',
          name: 'page-maintenance',
          component: () => import('@/views/pages/Maintenance.vue'),
          meta: {
            rule: 'isPublic'
          }
        }
      ]
    },
    // Redirect to 404 page, if no match found
    // RELEASE TODO
    {
      path: '*',
      redirect: '/pages/error-404'
    }
  ]
})

router.afterEach(() => {
  // Remove initial loading
  const appLoading = document.getElementById('loading-bg')
  if (appLoading) {
    appLoading.style.display = 'none'
  }
})
// RELEASE: redirect
router.beforeEach((to, from, next) => {
  // redirect to login page if not logged in and trying to access a restricted page
  const publicPages = [
    '/login',
    '/forgot-password',
    '/reset-password',
    '/register',
    '/pages/error-404',
    '/pages/error-500',
    '/pages/not-authorized',
    '/pages/comingsoon',
    '/admin*',
    '/api*'
  ]
  const authRequired = !publicPages.includes(to.path)
  const loggedIn = localStorage.getItem('userInfo')

  if (authRequired && !loggedIn) {
    return next({
      path: '/login',
      query: { returnUrl: to.path }
    })
  }

  next()
})

export default router
