const winston = require('winston');
const { format } = require('logform');

const pythonLogFormat = format.printf((info) => {
  return `[${info.label}] ${info.level}: ${info.message}`;
});
const electronLogFormat = format.printf((info) => {
  return `${info.timestamp} [${info.label}] ${info.level}: ${info.message}`;
});

const electronLogger = winston.createLogger({
  level: 'debug',
  format: format.combine(
    format.label({ label: 'Electron' }),
    format.timestamp(),
    electronLogFormat,
  ),
  transports: [
    new winston.transports.Console(),
  ],
});

const pythonAppLogger = winston.createLogger({
  level: 'debug',
  format: format.combine(
    format.label({ label: 'PythonServer' }),
    pythonLogFormat,
  ),
  transports: [
    new winston.transports.Console(),
  ],
});

module.exports = {
  electronLogger,
  pythonAppLogger,
};
