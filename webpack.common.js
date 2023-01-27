const MiniCssExtractPlugin = require("mini-css-extract-plugin")
const VueLoaderPlugin = require('vue-loader/lib/plugin')
const BundleTracker = require('webpack-bundle-tracker')
const appName = 'app'
const path = require("path")
const webpack = require('webpack')


module.exports = {
    entry: {
        app: './' + appName + '/static/js/index_app.js',
    },
    output: {
        path: path.resolve('./' + appName + '/static/bundles/'),
        filename: '[name]-[hash].js',
    },
    plugins: [
        new VueLoaderPlugin(),
        new webpack.ProvidePlugin({
            $: 'jquery',
            jQuery: 'jquery',
        }),
        new BundleTracker({
            path: __dirname,
            filename: './webpack-stats.json'
        }),
        new MiniCssExtractPlugin({
            filename: '[name]-[hash].css',
            chunkFilename: '[id].css',
        }),
    ],
    module: {
        rules: [{
                test: /\.scss$/,
                use: [{
                        loader: MiniCssExtractPlugin.loader,
                    },
                    {
                        loader: "css-loader"
                    },
                    {
                        loader: "sass-loader",
                    }
                ]
            },
            {
                test: /\.css$/,
                use: ['vue-style-loader', 'css-loader']
            },
            {
                test: /\.vue$/,
                loader: 'vue-loader',
                options: {
                    loaders: {
                        css: 'css-loader'
                    }
                }
            }
        ]
    }
}
