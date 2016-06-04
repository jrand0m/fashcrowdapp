module.exports = {
    entry: "./app/index.js",
    output: {
        path: __dirname,
        filename: "./dist/app.compiled.js"
    },
    module: {
        loaders: [
            { test: /\.jade$/, loaders: ["babel?presets[]=es2015", "jade"] },
            {
                test: /\.js$/,
                exclude: /(node_modules|bower)/,
                loader: "babel?presets[]=es2015&plugins[]=transform-decorators-legacy&plugins[]=transform-flow-strip-types"
            }
        ]
    },
    resolve: {
        root: __dirname + '/app',
        moduleDirectories: [__dirname + "/app"],
        alias: {
            "bootstrap": __dirname + "/app/bower/bootstrap-sass/assets/javascripts/bootstrap"
        }
    }
};