const BundleTracker = require('webpack-bundle-tracker')

process.env.VUE_APP_VERSION = require('./package.json').version

module.exports = {
  publicPath: 'http://localhost:8080/',
  outputDir: './dist/',

  chainWebpack: config => {
    config.optimization
      .delete('splitChunks')

    config
      .plugin('BundleTracker')
      .use(BundleTracker, [{ filename: '../frontend/webpack-stats.json' }])

    config.resolve.alias
      .set('__STATIC__', 'static')

    config.devServer
      .public('http://localhost:8080')
      .host('localhost')
      .port(8080)
      .hotOnly(true)
      .watchOptions({ poll: 1000 })
      .https(false)
      .headers({ 'Access-Control-Allow-Origin': ['\*'] })
  }

  // uncomment before executing 'npm run build'
  // css: {
  //   extract: {
  //     filename: 'bundle.css',
  //     chunkFilename: 'bundle.css'
  //   }
  // }
}
