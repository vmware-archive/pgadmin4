const isDocker = require('is-docker')();
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
            './src/**/*.js'
        ],
        preprocessors: {
            'src/**/*.js': ['babel'],
            'test/**/*.js': ['babel']
        },
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
         * We want to run the tests using the PhantomJS headless browser.
         * This is especially useful for continuous integration.
         */
        browsers: ['Chrome'],

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

        /**
         * List of plugins
         */
        plugins: [
            'karma-chrome-launcher',
            'karma-jasmine',
            'karma-jasmine-html-reporter',
            'karma-babel-preprocessor'
        ],
    });
};