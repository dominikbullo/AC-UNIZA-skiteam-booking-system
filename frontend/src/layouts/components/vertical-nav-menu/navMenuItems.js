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
            url: '/apps/family/members',
            name: 'Members',
            slug: 'app-family-members',
            i18n: 'Members'
          },
          {
            url: '/apps/family/view',
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
    name: 'Users',
    icon: 'UsersIcon',
    i18n: 'Users'
  },
  {
    url: '/page/statistics',
    name: 'Statistics',
    icon: 'PieChartIcon',
    slug: 'page-stats',
    i18n: 'Statistics'
  }
]
