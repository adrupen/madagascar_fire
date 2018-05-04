http = require('http');
fs = require('fs');

var execSync = require('child_process').execSync;

var GEOSS_url = "http://arduino.geodab.eu/gpw/procedure/6";
var today = new Date();

server = http.createServer( function(req, res) {

	res.setHeader("Access-Control-Allow-Origin", "http://127.0.0.1:8080");

    console.dir(req.param);

    if (req.method == 'POST') {
        console.log("POST");
        var body = '';
        req.on('data', function (data) {
            body += data;
            console.log("Partial body: " + body);
        });
        req.on('end', function () {
        	var params = body.split("&");
        	var timestamp = today.toISOString().substring(0, 10) + " " + today.toISOString().substring(11, 19);
        	var headers = "timestamp,";
        	var values = '"' + timestamp + '",';

        	for(var i=1; i<params.length; i++){
        		var p = params[i].split("=");
        		console.log(p);
        		headers += p[0] + ",";
        		values += '"' + p[1] + '",';
        	}
        	headers = headers.substring(0,headers.length-1) + "\n";
        	values = values.substring(0,values.length-1);

        	console.log("headers: "+headers);
        	console.log("values: "+values);

        	fs.writeFile("./py/ranger_report.csv", headers+values, function(err) {
			    if(err) {
			        return console.log(err);
			    }
			    console.log("./py/ranger_report.csv was saved");
			    var result = execSync("python ./py/upload_arduino.py ./py/ranger_report.csv "+GEOSS_url, {stdio:[0,1,2]});
			});
        });
        res.writeHead(200, {'Content-Type': 'text/html'});
        res.end('post received');
    }

});

port = 8089;
host = '127.0.0.1';
server.listen(port, host);
console.log('Listening at http://' + host + ':' + port);