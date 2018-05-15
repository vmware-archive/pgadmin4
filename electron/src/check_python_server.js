const axios = require('axios');
const logger = require('winston');

function checkIfPythonServerIsRunning(functionToExecuteWhenApplicationIsUp) {
  return axios.get('http://localhost:5050')
        .then(() => {
          functionToExecuteWhenApplicationIsUp();
        })
        .catch((error) => {
          logger.error(error.message);
          const promise = new Promise((resolve, reject) => {
            setTimeout(() => {
              checkIfPythonServerIsRunning(functionToExecuteWhenApplicationIsUp)
                        .then((result) => {
                          resolve(result);
                        })
                        .catch((result) => {
                          reject(result);
                        });
            }, 1000);
          });

          return promise;
        });
}

module.exports = {
  checkIfPythonServerIsRunning,
};
