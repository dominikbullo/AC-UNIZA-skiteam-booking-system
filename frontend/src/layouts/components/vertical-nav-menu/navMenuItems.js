/* =========================================================================================
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
========================================================================================== */


export default [
  {
    url: '/dashboard',
    name: 'Dashboard',
    icon: 'HomeIcon',
    i18n: 'Dashboard'
  },
  {
    header: 'Apps',
    icon: 'PackageIcon',
    i18n: 'Apps',
    items: [
      {
        url: '/apps/event/calendar',
        name: 'Calendar',
        slug: 'app-event-calendar',
        icon: 'CalendarIcon',
        tagColor: 'success',
        i18n: 'Calendar'
      },
      {
        url: null,
        name: 'Family',
        icon: 'UsersIcon',
        i18n: 'Family',
        submenu: [
          {
            url: '/apps/family/list',
            name: 'List',
            slug: 'app-family-list',
            i18n: 'List'
          },
          {
            url: '/apps/family/view/1',
            name: 'View',
            slug: 'app-family-view',
            i18n: 'View'
          }
        ]
      }
    ]
  },
  {
    url: '/apps/user/user-list',
    slug: 'page-user-settings',
    name: 'Members',
    icon: 'UsersIcon',
    i18n: 'Members'
  },
  {
    url: '/apps/user/user-view/268',
    name: 'View',
    slug: 'app-user-view',
    icon: 'UserIcon',
    i18n: 'User Views TEST'
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
          }
        ]
      }
    ]
  }
  // {
  //   header: 'Others',
  //   icon: 'MoreHorizontalIcon',
  //   i18n: 'Others',
  //   items: [
  //     {
  //       url: '/pages/faq',
  //       slug: 'page-faq',
  //       name: 'FAQ',
  //       icon: 'HelpCircleIcon',
  //       i18n: 'FAQ'
  //     }
  //   ]
  // }
]
