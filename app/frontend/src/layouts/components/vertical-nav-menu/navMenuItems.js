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
  // {
  //   url: "/apps/email",
  //   name: "Email",
  //   slug: "email",
  //   icon: "MailIcon",
  //   i18n: "Email",
  // },
  {
    url: "/",
    name: 'Dashboard',
    tag: '2',
    tagColor: 'warning',
    icon: 'HomeIcon',
    i18n: 'Dashboard',
  },
  {
    header: 'Apps',
    icon: 'PackageIcon',
    i18n: 'Apps',
    items: [
      {
        url: '/apps/calendar/vue-simple-calendar',
        isDisabled: true,
        name: 'Calendar',
        slug: 'calendar-simple-calendar',
        icon: 'CalendarIcon',
        tagColor: 'success',
        i18n: 'Calendar'
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
    header: 'Pages',
    icon: 'FileIcon',
    i18n: 'Pages',
    items: [
      {
        url: "/page2",
        name: "Page 2",
        slug: "page2",
        icon: "FileIcon",
      },
      {
        url: '/pages/profile',
        isDisabled: true,
        slug: 'page-profile',
        name: 'Profile',
        icon: 'UserIcon',
        i18n: 'Profile'
      },
      {
        url: '/pages/user-settings',
        slug: 'page-user-settings',
        name: 'User Settings',
        icon: 'SettingsIcon',
        i18n: 'UserSettings'
      },
      {
        url: '/pages/search',
        isDisabled: true,
        slug: 'page-search',
        name: 'Search',
        icon: 'SearchIcon',
        i18n: 'Search'
      },
      {
        url: null,
        name: 'Miscellaneous',
        icon: 'CoffeeIcon',
        i18n: 'Miscellaneous',
        submenu: [
          {
            url: '/pages/not-authorized',
            name: 'Not Authorized',
            slug: 'page-not-authorized',
            icon: 'XCircleIcon',
            i18n: 'NotAuthorized',
            target: '_blank'
          },
          {
            url: '/pages/maintenance',
            name: 'Maintenance',
            slug: 'page-maintenance',
            icon: 'AnchorIcon',
            i18n: 'Maintenance',
            target: '_blank'
          },
          {
            url: '/pages/comingsoon',
            slug: 'page-coming-soon',
            name: 'Coming Soon',
            icon: 'ClockIcon',
            i18n: 'ComingSoon',
            target: '_blank'
          },
          {
            url: '/pages/error-404',
            name: '404',
            slug: 'page-error-404',
            i18n: '404',
            target: '_blank'
          },
          {
            url: '/pages/error-500',
            name: '500',
            slug: 'page-error-500',
            i18n: '500',
            target: '_blank'
          }
        ]
      }
    ]
  },
  {
    header: 'Charts',
    icon: 'PieChartIcon',
    i18n: 'ChartsAndMaps',
    items: [
      {
        url: null,
        name: 'Charts',
        icon: 'PieChartIcon',
        tag: '3',
        tagColor: 'success',
        i18n: 'Charts',
        isDisabled: true,
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
  {
    header: 'Others',
    icon: 'MoreHorizontalIcon',
    i18n: 'Others',
    items: [
      {
        url: null,
        name: 'Disabled Menu',
        icon: 'EyeOffIcon',
        i18n: 'DisabledMenu',
        isDisabled: true
      },
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

