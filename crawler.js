var fs = require('fs');
var system = require('system');

var page = require('webpage').create();

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

// Log response to resource requests in the same json object by url
var onResourceReceived = function(response) {
    resJson[response['url']] = {};
    resJson[response['url']]['response'] = response;
};

var onLoadFinished = function() {
    console.log("onLoadFinished");
    var pageWidth = page.viewportSize.width;
    var pageHeight = page.viewportSize.height;
    console.log(pageWidth + "," + pageHeight);
    for (var dmy = 0; dmy < totalClicks; dmy++) {
         setTimeout(function() {
             var clickX = pageWidth / 2;
             var clickY = pageHeight / 4;
             console.log('clickX: ' + clickX + ' clickY: ' + clickY);
            // page.sendEvent('click', page.clipRect.width / 4 + (Math.random() * page.clipRect.width / 2), page.clipRect.height / 4 + (Math.random() * page.clipRect.height / 2));
            page.sendEvent('click', clickX, clickY);
            page.render('image' + numClicksLeft + '.png');
            numClicksLeft--;
            if (numClicksLeft == 0) {
                finish();
            }
        }, (Math.random() * 500));
     }
     fs.write(errorFile, JSON.stringify(errorJson, 4, null), 'w');
     fs.write(resFile, JSON.stringify(resJson, 4, null), 'w');
};

// Logic for when pop ups are opened
var onPageCreated = function(newPage) {
    console.log('New page created');
    console.log(newPage.url);
};

var finish = function() {
    time = Date.now() - time;
    console.log('Time taken to crawl ' + website + ': ' + time + ' ms');
    setTimeout(function() { phantom.exit(); }, 1500);
    // phantom.exit();
};

// Open the page
var time = Date.now();
var numClicksLeft = 20;
var totalClicks = numClicksLeft;

page.onError = onError;
page.onResourceRequested = onResourceRequested;
page.onResourceReceived = onResourceReceived;
page.onLoadFinished = onLoadFinished;
page.onPageCreated = onPageCreated;
 
page.open(website);

