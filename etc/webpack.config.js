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
                loader: "babel?presets[]=es2015"
            }
        ]
    },
    resolve: {
        root: __dirname,
        moduleDirectories: [__dirname + "/app"],
        alias: {
            "jquery$": __dirname + "/bower/jquery/dist/jquery.js",
            "bootstrap": __dirname + "/bower/bootstrap/dist"
        }
    }
};