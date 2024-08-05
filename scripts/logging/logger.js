"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var fs_1 = require("fs");
var path_1 = require("path");
var logDir = path_1.default.resolve(__dirname, '../../logs');
var logFile = path_1.default.join(logDir, 'pipeline.log');
if (!fs_1.default.existsSync(logDir)) {
    fs_1.default.mkdirSync(logDir, { recursive: true });
}
function logMessage(message) {
    var timestamp = new Date().toISOString();
    var logEntry = "".concat(timestamp, " - ").concat(message, "\n");
    fs_1.default.appendFileSync(logFile, logEntry);
}
var message = process.argv[2];
logMessage(message);
exports.default = logMessage;
