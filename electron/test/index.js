const Application = require('spectron').Application;
const electron = require('electron');
const path = require('path');
const waitForPythonServerToBeAvailable = require('../src/check_python_server');

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
        path.join(__dirname, '..'),
      ],
      waitTimeout: 50000,
    });
    chaiAsPromised.transferPromiseness = app.transferPromiseness;
    return app.start();
  });

  after(() => {
    if (app && app.isRunning()) {
      return app.stop();
    }

    return new Promise((resolve) => { return resolve(); });
  });

  it('lets the user know that pgadmin is loading', () => {
    return app.client.waitUntilWindowLoaded()
      .getText('body').should.eventually.equal('pgAdmin4 Loading...');
  });

  describe('when the server is available', () => {
    it('loading window is no longer present', () => {
      return waitForPythonServerToBeAvailable.waitForPythonServerToBeAvailable(() => {
        return app.browserWindow.isVisible().should.eventually.be.false;
      });
    }).timeout(40000);
  });
});
