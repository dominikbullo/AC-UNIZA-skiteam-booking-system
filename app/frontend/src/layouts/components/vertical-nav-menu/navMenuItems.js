/*=========================================================================================
  File Name: sidebarItems.js
  Description: Sidebar Items list. Add / Remove menu items from here.
  Strucutre:
          url     => router path
          name    => name to display in sidebar
          slug    => router path name
          icon    => Feather Icon component/icon name
          tag     => text to display on badge
          tagColor  => class to apply on badge element
          i18n    => Internationalization
          submenu   => submenu of current item (current item will become dropdown )
                NOTE: Submenu don't have any icon(you can add icon if u want to display)
          isDisabled  => disable sidebar item/group
  ----------------------------------------------------------------------------------------
  Item Name: Vuexy - Vuejs, HTML & Laravel Admin Dashboard Template
  Author: Pixinvent
  Author URL: http://www.themeforest.net/user/pixinvent
==========================================================================================*/


export default [
  {
    url: '/dashboard',
    name: 'Dashboard',
    // tag: '2',
    tagColor: 'warning',
    icon: 'HomeIcon',
    i18n: 'Dashboard'
  },
  {
    header: 'Apps',
    icon: 'PackageIcon',
    i18n: 'Apps',
    items: [
      {
        url: null,
        name: 'Events',
        icon: 'CalendarIcon',
        // eslint-disable-next-line no-invalid-this
        i18n: 'Events',
        submenu: [
          {
            url: '/apps/event/list',
            name: 'List',
            slug: 'app-event-list',
            i18n: 'List'
          },
          {
            url: '/apps/calendar',
            name: 'Calendar',
            slug: 'calendar',
            icon: 'CalendarIcon',
            tagColor: 'success',
            i18n: 'Calendar'
          }
        ]
      },
      {
        url: null,
        name: 'Users',
        icon: 'UsersIcon',
        // eslint-disable-next-line no-invalid-this
        i18n: 'Users',
        submenu: [
          {
            url: '/apps/user/user-list',
            name: 'app-user-list',
            slug: 'app-user-list',
            i18n: 'List'
          },
          {
            url: '/apps/user/user-edit/268',
            name: 'Edit',
            slug: 'app-user-edit',
            i18n: 'Edit'
          }
        ]
      }
    ]
  },
  {
    header: 'Pages',
    icon: 'FileIcon',
    i18n: 'Pages',
    items: [
      {
        url: '/pages/user-settings',
        slug: 'page-user-settings',
        name: 'Account',
        icon: 'SettingsIcon',
        i18n: 'Account'
      },
      {
        url: '/pages/family-settings',
        slug: 'family-settings',
        name: 'Family',
        icon: 'UsersIcon',
        i18n: 'Family'
      },
      {
        url: '/testpage',
        name: 'Test Page',
        slug: 'test-page',
        icon: 'FileIcon'
      }
      // , {
      //   url: '/pages/profile',
      //   slug: 'page-profile',
      //   name: 'Profile',
      //   icon: 'UserIcon',
      //   i18n: 'Profile'
      // }
    ]
  },
  {
    header: 'Charts',
    icon: 'PieChartIcon',
    i18n: 'Charts',
    items: [
      {
        url: null,
        name: 'Charts',
        icon: 'PieChartIcon',
        tag: '3',
        tagColor: 'success',
        i18n: 'Charts',
        submenu: [
          {
            url: '/charts-and-maps/charts/apex-charts',
            name: 'Apex Charts',
            slug: 'extra-component-charts-apex-charts',
            i18n: 'ApexCharts'
          },
          {
            url: '/charts-and-maps/charts/chartjs',
            name: 'chartjs',
            slug: 'extra-component-charts-chartjs',
            i18n: 'chartjs'
          },
          {
            url: '/charts-and-maps/charts/echarts',
            name: 'echarts',
            slug: 'extra-component-charts-echarts',
            i18n: 'echarts'
          }
        ]
      }
    ]
  },
  // TODO show this only for admins
  // everything wit /admin/
  {
    header: 'Admin',
    icon: 'PackageIcon',
    i18n: 'Admin',
    items: [
      {
        url: '/admin/dashboard',
        name: 'Admin dashboard',
        // tag: '2',
        tagColor: 'warning',
        icon: 'HomeIcon',
        i18n: 'Admin dashboard'
      },
      {
        url: null,
        name: 'Events',
        icon: 'CalendarIcon',
        i18n: 'Event',
        submenu: [
          {
            url: '/apps/event/list',
            name: 'List',
            slug: 'app-event-list',
            i18n: 'List'
          },
          {
            url: '/apps/calendar/vue-simple-calendar',
            name: 'Calendar',
            slug: 'calendar-simple-calendar',
            icon: 'CalendarIcon',
            tagColor: 'success',
            i18n: 'Calendar'
          }
        ]
      },
      {
        url: null,
        name: 'User',
        icon: 'UserIcon',
        i18n: 'User',
        submenu: [
          {
            url: '/apps/user/user-list',
            name: 'List',
            slug: 'app-user-list',
            i18n: 'List'
          },
          {
            url: '/apps/user/user-view/268',
            name: 'View',
            slug: 'app-user-view',
            i18n: 'View'
          },
          {
            url: '/apps/user/user-edit/268',
            name: 'Edit',
            slug: 'app-user-edit',
            i18n: 'Edit'
          }
        ]
      }
    ]
  },
  {
    header: 'Others',
    icon: 'MoreHorizontalIcon',
    i18n: 'Others',
    items: [
      // {
      //   url: null,
      //   name: 'Disabled Menu',
      //   icon: 'EyeOffIcon',
      //   i18n: 'DisabledMenu',
      //   isDisabled: true
      // },
      {
        url: null,
        name: 'Support',
        icon: 'SmileIcon',
        i18n: 'Support',
        submenu: [
          {
            url: 'https://pixinvent.com/demo/vuexy-vuejs-admin-dashboard-template/documentation/',
            name: 'Documentation',
            icon: 'BookOpenIcon',
            slug: 'external',
            i18n: 'Documentation',
            target: '_blank'
          },
          {
            url: 'https://pixinvent.ticksy.com/',
            name: 'Raise Support',
            icon: 'LifeBuoyIcon',
            slug: 'external',
            i18n: 'RaiseSupport',
            target: '_blank'
          }
        ]
      }
    ]
  }
]
