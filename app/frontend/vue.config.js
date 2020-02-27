/*=========================================================================================
  File Name: vue.config.js
  Description: configuration file of vue
  ----------------------------------------------------------------------------------------
  Item Name: Vuexy - Vuejs, HTML & Laravel Admin Dashboard Template
  Author: Pixinvent
  Author URL: http://www.themeforest.net/user/pixinvent
==========================================================================================*/
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
  }
}


const BundleTracker = require('webpack-bundle-tracker')

module.exports = {
  // on Windows you might want to set publicPath: "http://127.0.0.1:8080/"
  publicPath: 'http://localhost:8080/',
  outputDir: './dist/',

  chainWebpack: config => {

    config
      .plugin('BundleTracker')
      .use(BundleTracker, [{filename: './webpack-stats.json'}])

    config.output
      .filename('bundle.js')

    config.optimization
      .splitChunks(false)

    config.resolve.alias
      .set('__STATIC__', 'static')

    config.devServer
    // the first 3 lines of the following code have been added to the configuration
      .public('http://127.0.0.1:8080')
      .host('127.0.0.1')
      .port(8080)
      .hotOnly(true)
      .watchOptions({poll: 1000})
      .https(false)
      .disableHostCheck(true)
      .headers({'Access-Control-Allow-Origin': ['\*']})

  }

  // uncomment before executing 'npm run build'
  // css: {
  //     extract: {
  //       filename: 'bundle.css',
  //       chunkFilename: 'bundle.css',
  //     },
  // }

}
