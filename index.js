/**
 * @ Lamosty.com 2016
 */

"use strict";

let PythonShell = require('python-shell');

let options = {
	mode: 'json',
	pythonOptions: ['-u'] // don't buffer the output of print
};

let pulsesToDataShell = new PythonShell('pulses_to_data.py', options)

pulsesToDataShell.on('message', (message) => {
	console.log(message);
});

pulsesToDataShell.end((err) => {
});

setTimeout(() => {

	pulsesToDataShell.childProcess.kill()

}, 5000);



