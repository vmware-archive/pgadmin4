const Application = require('spectron').Application;
const electron = require('electron');
const path = require('path');

const chai = require('chai');
const chaiAsPromised = require('chai-as-promised');

chai.should();
chai.use(chaiAsPromised);

describe('pgAdmin4', () => {

    let app;

    before(() => {
        app = new Application({
            path: electron,
            args: [
                path.join(__dirname, '..')
            ],
            waitTimeout: 50000
        });
        chaiAsPromised.transferPromiseness = app.transferPromiseness;
        return app.start();
    });

    after(() => {
        if (app && app.isRunning()) {
            return app.stop()
        }
    });

    it('lets the user know that pgadmin is loading', () => {
        return app.client.waitUntilWindowLoaded()
            .getText('body').should.eventually.equal('pgAdmin4 Loading...');
    });
});
