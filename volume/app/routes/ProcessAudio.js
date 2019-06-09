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
    let {text, region} = req.body;

    voice_file = 'voices/20170428.htsvoice'
    if (region != undefined){
        voice_file = 'voices/' + region + '/speech.htsvoice'
    }

    async.waterfall([
        function(cb) {
            if (fs.existsSync(voice_file)) {
                console.log(voice_file);
            }
            else {
                console.log("hts file not found")
                voice_file = 'voices/20170428.htsvoice'
            }
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

router.post('/human', (req, res) => {
    let {region, scriptCode} = req.body;

    human_voice_file = 'voices/' + region + '/' + scriptCode + '.wav'
    try {
        if (fs.existsSync(human_voice_file)) {
            sendFile(human_voice_file, res);
        }
        else {
            console.log("file not found");
            res.status(404).send();
        }
      } catch(err) {
        console.error(err);
      }
    
});

module.exports = router;