const isDocker = require('is-docker')();
const webpackConfiguration = require('./webpack.config');
/**
 * This is the Karma configuration file. It contains information about this skeleton
 * that provides the test runner with instructions on how to run the tests and
 * generate the code coverage report.
 *
 * For more info, see: http://karma-runner.github.io/0.12/config/configuration-file.html
 */
module.exports = function (config) {
    config.set({
        /**
         * These are the files required to run the tests.
         *
         * The `Function.prototype.bind` polyfill is required by PhantomJS
         * because it uses an older version of JavaScript.
         */
        files: [
            './src/**/*_spec.js'
        ],
        babelPreprocessor: {
            options: {
                presets: ['env'],
                sourceMap: 'inline'
            },
            filename: function (file) {
                return file.originalPath.replace(/\.js$/, '.es5.js');
            },
            sourceFileName: function (file) {
                return file.originalPath;
            }
        },

        /**
         * Use Mocha as the test framework, Sinon for mocking, and
         * Chai for assertions.
         */
        frameworks: ['jasmine'],

        /**
         * After running the tests, return the results and generate a
         * code coverage report.
         */
        reporters: ['progress', 'kjhtml'],

        autoWatch: true,
        usePolling: true,

        // start these browsers
        // available browser launchers: https://npmjs.org/browse/keyword/karma-launcher
        customLaunchers: {
            ChromeCustom: {
                base: 'ChromeHeadless',
                // We must disable the Chrome sandbox when running Chrome inside Docker (Chrome's sandbox needs
                // more permissions than Docker allows by default)
                flags: isDocker ? ['--no-sandbox'] : [],
            },
        },
        browsers: ['ChromeCustom'],
        /*karma-webpack config*/
        preprocessors: {
            //use webpack to support require() in test-suits .js files
            //use babel-loader from webpack to compile es2015 features in .js files
            //add webpack as preprocessor
            './src/**/*.js': ['webpack']
        },
        webpackMiddleware: {
            //turn off webpack bash output when run the tests
            noInfo: true,
            stats: 'errors-only'
        },
        webpack: webpackConfiguration,
        /**
         * List of plugins
         */
        plugins: [
            'karma-chrome-launcher',
            'karma-jasmine',
            'karma-jasmine-html-reporter',
            'karma-babel-preprocessor',
            'karma-webpack',
            'karma-electron'
        ],
    });
};
