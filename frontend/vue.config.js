/* =========================================================================================
  File Name: vue.config.js
  Description: configuration file of vue
  ----------------------------------------------------------------------------------------
  Item Name: Vuexy - Vuejs, HTML & Laravel Admin Dashboard Template
  Author: Pixinvent
  Author URL: http://www.themeforest.net/user/pixinvent
========================================================================================== */


module.exports = {
  publicPath: '/',
  transpileDependencies: [
    'vue-echarts',
    'resize-detector'
  ],
  configureWebpack: {
    optimization: {
      splitChunks: {
        chunks: 'all'
      }
    }
  },
  outputDir: 'dist',
  assetsDir: 'static',
  // baseUrl: IS_PRODUCTION
  // ? 'http://cdn123.com'
  // : '/',
  // For Production, replace set baseUrl to CDN
  // And set the CDN origin to `yourdomain.com/static`
  // Whitenoise will serve once to CDN which will then cache
  // and distribute
  devServer: {
    proxy: {
      '/api*': {
        // Forward frontend dev server request for /api to django dev server
        target: 'http://localhost:8000/'
        // secure: false,
        // logLevel: 'debug'
      }
    }
  }
}

module.exports = {
  // ...other vue-cli plugin options...
  pwa: {
    name: 'AC UNIZA Ski Team',
    themeColor: '#00b0d3',
    msTileColor: '#000000',
    appleMobileWebAppCapable: 'yes',
    appleMobileWebAppStatusBarStyle: 'black'
  }
}

