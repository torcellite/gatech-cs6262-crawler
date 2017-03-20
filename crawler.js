var fs = require('fs');
var system = require('system');

var page = require('webpage').create();
// Set user-agent
page.settings.userAgent = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36';
// Viewport size
page.viewportSize = {width: 500, height: 2500};
var pageWidth = page.viewportSize.width;
var pageHeight = page.viewportSize.height;
 

var website = system.args[1];
var directory = 'crawled_websites/';
if (website.substr(0, 5) === 'https') { 
    directory = 'crawled_websites/' + website.substr(8);
} else {
    directory = 'crawled_websites/' + website.substr(7);
}

// Create a directory for the website to be crawled
fs.makeDirectory(directory);

var errorJson = [];
var resJson = {};
var errorFile = directory + '/error.json';
var resFile = directory + '/resources.json';

// Log page errors in a JSON object
var onError = function(msg, trace) {
    var error = {};
    error['msg'] = msg;
    error['trace'] = trace;
    errorJson.push(error);
};

// Log resource requests in a json object by url
var onResourceRequested = function(request) {
    resJson[request['url']] = {};
    resJson[request['url']]['request'] = request;
};

var contentTypeWhitelist = ['application/json', 'application/javascript', 'application/x-javascript', 'application/font-woff'];
// Log response to resource requests in the same json object by url
var onResourceReceived = function(response) {
    resJson[response['url']] = {};
    resJson[response['url']]['response'] = response;

    // Check if the file being requested is an application - possible malware
    if (response['contentType'].substr(0, 11) === 'application') {
        var malicious = true;
        for (var idx = 0; idx < contentTypeWhitelist.length; idx++) {
            if (response['contentType'].indexOf(contentTypeWhitelist[idx]) !== -1) {
                malicious = false;
                break;
            }
        }    
        if (malicious) {
            console.log(response['url'] + ' ' + response['contentType']);
            console.log('Download link found');
        }
    }
};

var onLoadFinished  = function() {
    // Create click grid
    for (var x = gridSize / 2; x < pageWidth; x += gridSize) {
        for (var y = gridSize / 2; y < pageHeight; y += gridSize) {
            clickPage(x, y);
       }
    }
    fs.write(errorFile, JSON.stringify(errorJson, 4, null), 'w');
    fs.write(resFile, JSON.stringify(resJson, 4, null), 'w');
};

// Logic for when pop ups are opened
var onPageCreated = function(newPage) {
    console.log('New page created');
    console.log(newPage.url);
};

var onNavigationRequested = function(url, type, willNavigate, main) {
    console.log('Trying to navigate to: ' + url + ' from: ' + page.url);
//    console.log('Caused by: ' + type);
//    console.log('Will actually navigate: ' + willNavigate);
//    console.log('Sent from the page\'s main frame: ' + main);
};

var gridSize = 250;
var clicksCompleted = 0;
var clickPage = function(x, y) {
    setTimeout(function() {
//        console.log('x: ' + x + ' y: ' + y);
        clicksCompleted++;
        page.sendEvent('click', x, y);
        page.render('image' + clicksCompleted + '.png');
        // Minus 2 to account for grid sizes that are not factors of the viewport dimensions
        if (clicksCompleted >= (pageWidth * pageHeight / (gridSize * gridSize)) - 2) {
            finish();
        }
    }, (Math.random() * 500)); 
};

var finish = function() {
    time = Date.now() - time;
    console.log('Time taken to crawl ' + website + ': ' + time + ' ms');
    setTimeout(function() { phantom.exit(); }, 1500);
};

page.onError = onError;
page.onResourceRequested = onResourceRequested;
page.onResourceReceived = onResourceReceived;
page.onLoadFinished = onLoadFinished;
page.onPageCreated = onPageCreated;
page.onNavigationRequested = onNavigationRequested;

// Open the page
var time = Date.now(); 
page.open(website, function(status) {
    if (status === 'success') {
        console.log('Opened ' + page.url);
    } else {
        console.log('Could not open ' + page.url);
    }
});

