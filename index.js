/**
 * @ Lamosty.com 2016
 */

"use strict";

let PythonShell = require('python-shell');

let options = {
	mode: 'json',
	pythonOptions: ['-u']
};

let pulsesToDataShell = PythonShell.run('pulses_to_data.py', options, (err) => {
	if (err) {
		throw err;
	}
});

pulsesToDataShell.on('message', (message) => {
	console.log(message);
});

pulsesToDataShell.end((err) => {
	if (err) {
		console.log(err);
	}

	console.log('finished');
});


