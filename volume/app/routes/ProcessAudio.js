var express = require('express'),
    router = express.Router(),
	scriptDB = require('../db/Script'),
    async = require("async"),
	childProcess= require("child_process"),
    fs = require('fs');

const sendFile = (filePath, res) => {
    const file = fs.createReadStream(filePath);
    file.pipe(res);
}


router.post('/', (req, res) => {
    let {text} = req.body;

    voice_file = 'voices/20170428.htsvoice'
    async.waterfall([
        function(cb) {
            var spawn = childProcess.spawn;
            var fileName = 'output/sound_' + Math.floor(Math.random()*1000) + '-' + Date.now() + '.wav';
            var process = spawn('python3',
            ["./python/textToSound.py", 
            '-t', text, 
            '-v', voice_file, 
            '-o', fileName], {detached: true});
    
            var timeout = setTimeout(() => {
                try {
                    process.kill(-child.pid, 'SIGKILL');
                } catch (e) {
                    console.log('Cannot kill process');
                }
            }, 15000);

            gotData = false
            process.on('error', err => console.log('Error:', err));
            process.on('exit', () => { clearTimeout(timeout); if (!gotData) {cb('Timeout', null);}});
		    process.stdout.on('data', function(data) {
                gotData = true
                
                rs = data.toString();
                rs = rs.trim();
                if (rs == 'success') {
                    cb(null, fileName)
                }
			});
        
        }, 
    ], function(err, result) { 
        if (err) {
            res.send({
                status: 400,
                message: err
            });
        } else{
            sendFile(result, res);
        }
    })
});

module.exports = router;