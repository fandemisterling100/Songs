  const appName = 'app'
  const common = require('./webpack.common.js');
  const { merge } = require('webpack-merge');
  const path = require("path")
  const RelativeBundleTrackerPlugin = require('./RelativeBundleTrackerPlugin')


  module.exports = merge(common, {
      mode: 'development',
      devtool: 'inline-source-map',
      output: {
          path: path.resolve('./' + appName + '/static/bundles/'),
          filename: '[name]-[hash].js',
      },
      plugins: [
          new RelativeBundleTrackerPlugin({
              path: __dirname,
              filename: './webpack-stats.json'
          }),
      ]
  });
