/* =========================================================================================
  File Name: vue.config.js
  Description: configuration file of vue
  ----------------------------------------------------------------------------------------
  Item Name: Vuexy - Vuejs, HTML & Laravel Admin Dashboard Template
  Author: Pixinvent
  Author URL: http://www.themeforest.net/user/pixinvent
========================================================================================== */

const BundleTracker = require('webpack-bundle-tracker')

module.exports = {
  baseUrl: 'http://0.0.0.0:8080/',
  outputDir: './dist/',

  chainWebpack: config => {
    config.optimization
      .splitChunks(false)

    config
      .plugin('BundleTracker')
      .use(BundleTracker, [{ filename: './webpack-stats.json' }])

    config.resolve.alias
      .set('__STATIC__', 'static')

    config.devServer
      .public('http://127.0.0.1:8080')
      .host('127.0.0.1')
      .port(8080)
      .hotOnly(true)
      .watchOptions({ poll: 1000 })
      .https(false)
      .headers({ 'Access-Control-Allow-Origin': ['\*'] })
  },
  publicPath:
    '/',
  transpileDependencies:
    [
      'vue-echarts',
      'resize-detector'
    ],
  configureWebpack:
    {
      optimization: {
        splitChunks: {
          chunks: 'all'
        }
      }
    },
  // outputDir: 'dist',
  assetsDir:
    'static',
  // baseUrl: IS_PRODUCTION
  // ? 'http://cdn123.com'
  // : '/',
  // For Production, replace set baseUrl to CDN
  // And set the CDN origin to `yourdomain.com/static`
  // Whitenoise will serve once to CDN which will then cache
  // and distribute
  // devServer:
  //   {
  //     proxy: {
  //       '^/api':
  //         {
  //           target: 'http://localhost:8000',
  //           changeOrigin:
  //             true, // so CORS doesn't bite us.
  //           // secure: false,
  //           // pathRewrite: { '^/api': '/api' },
  //           logLevel:
  //             'debug'
  //         }
  //     }
  //   },
  pwa: {
    name: 'AC UNIZA Ski Team',
    themeColor:
      '#00b0d3',
    msTileColor:
      '#000000',
    appleMobileWebAppCapable:
      'yes',
    appleMobileWebAppStatusBarStyle:
      'black'
  }
}
