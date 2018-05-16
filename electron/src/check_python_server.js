const axios = require('axios');
const { electronLogger } = require('./logger');

function checkIfPythonServerIsAvailable() {
  return axios.get('http://localhost:5050')
    .then(() => {
      return true;
    })
    .catch(() => {
      return false;
    });
}

function delayedCheckIfServerIsAvailable(functionToExecuteWhenApplicationIsUp) {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      waitForPythonServerToBeAvailable(functionToExecuteWhenApplicationIsUp)
        .then((result) => {
          resolve(result);
        })
        .catch((result) => {
          reject(result);
        });
    }, 1000);
  });
}

function waitForPythonServerToBeAvailable(functionToExecuteWhenApplicationIsUp) {
  return checkIfPythonServerIsAvailable()
    .then((isAvailable) => {
      if (isAvailable) {
        return functionToExecuteWhenApplicationIsUp();
      }
      electronLogger.error('Server not available, waiting.....');
      return delayedCheckIfServerIsAvailable(functionToExecuteWhenApplicationIsUp);
    })
    .catch((error) => {
      electronLogger.error(`Error waiting for python server availability: ${error}\n ${error.stack}`);
    });
}

module.exports = {
  waitForPythonServerToBeAvailable,
};
