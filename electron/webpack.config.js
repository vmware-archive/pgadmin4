
module.exports = {
    module: {

    rules: [
        {
            test: /\.js$/,
            exclude: /(node_modules)/,
            loader: "babel-loader",
            query: {
                presets: ["env"]
            }
        }
    ]
    },
    node: {
        fs: "empty",
        child_process: "empty"
    }
}
