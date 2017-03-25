var maliciousPageCrawler = function(popupPage, url, finishCallback) {
  var page;
  if (popupPage === null) {
    page = require('webpage').create();
  } else {
    page = popupPage;
  }
  // Set user-agent
  page.settings.userAgent =
    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36';
  // Viewport size
  page.viewportSize = {
    width: 500,
    height: 2500
  };
  var pageWidth = page.viewportSize.width;
  var pageHeight = page.viewportSize.height;

  var website = url;
  var directory;
  // Check to ensure URL contains http/https
  if (url.substr(0, 7) === 'http://' || url.substr(0, 8) === 'https://') {
    directory = rootDirectory + '/' + url.split('/')[2] + '_' +
      numOfActivePopups;
  } else {
    directory = rootDirectory + '/' + url + '_' +
      numOfActivePopups;
    website = 'http://' + url;
  }
  // Create a directory for the website to be crawled
  fs.makeDirectory(directory);

  var errorJson = [];
  var errorFile = directory + '/error.json';
  // Log page errors in a JSON object
  var onError = function(msg, trace) {
    var error = {};
    error['msg'] = msg;
    error['trace'] = trace;
    errorJson.push(error);
  };

  var resJson = {};
  var resFile = directory + '/resources.json';
  // Log resource requests in a json object by url
  var onResourceRequested = function(request) {
    ++featureNumOfResourcesRequested;
    resJson[request['url']] = {};
    resJson[request['url']]['request'] = request;
  };

  var downloadsFolder = directory + '/downloads';
  var downloadRequestsFolder = directory + '/downloads/requests';
  // Create directories
  fs.makeDirectory(downloadsFolder);
  fs.makeDirectory(downloadRequestsFolder);

  var contentTypeWhitelist = ['application/json', 'application/javascript',
    'application/x-javascript', 'application/font-woff',
    'application/x-font-ttf',
    'application/x-font-opentype', 'application/x-font-truetype',
    'application/font-woff', 'application/font-woff2',
    'application/vnd.ms-fontobject', 'application/vnd.ms-fontobject'
  ];
  // Empty whitelist for debugging purposes
  // var contentTypeWhitelist = [];
  // Log response to resource requests in the same json object by url
  var onResourceReceived = function(response) {
    ++featureNumOfResourcesReceived;
    if (response.bodySize !== undefined)
      featureSizeOfResourcesReceived += response.bodySize;
    resJson[response['url']]['response'] = response;

    // Check if the file being requested is an application - possible malware
    if (response['contentType'].substr(0, 11) === 'application') {
      var malicious = true;
      for (var idx = 0; idx < contentTypeWhitelist.length; idx++) {
        if (response['contentType'].indexOf(contentTypeWhitelist[idx]) !==
          -1) {
          malicious = false;
          break;
        }
      }
      if (malicious) {
        ++featureNumOfNonWhitelistedResourcesReceived;
        if (response.bodySize !== undefined)
          featureSizeOfNonWhitelistedResourcesReceived += response.bodySize;
        var requestFile = downloadRequestsFolder + '/request-' + Date.now() +
          '.txt';
        var headers = resJson[response['url']]['request']['headers'];
        var requestFileContent = resJson[response['url']]['request'][
          'method'
        ] + '\n';
        requestFileContent += response['url'] + '\n';

        for (var idx = 0; idx < headers.length; idx++) {
          requestFileContent += headers[idx]['name'] + ': ' + headers[idx][
            'value'
          ] + '\n';
        }
        fs.write(requestFile, requestFileContent, 'w');
        if (DEBUG) console.log('Created request to download ' + response[
            'url'] +
          ' of content-type ' + response['contentType']);
      }
    }
  };

  var loadStartTime;
  var onLoadStarted = function() {
    loadStartTime = Date.now();
    if (DEBUG) console.log('Loading the new page');
  };

  var onLoadFinished = function() {
    ++numPagesLoaded;
    featureTotalLoadTime += (Date.now() - loadStartTime);
    page.render(directory + '_screenshot.png');
    // Create click grid
    for (var x = gridSize / 2; x < pageWidth; x += gridSize) {
      for (var y = gridSize / 2; y < pageHeight; y += gridSize) {
        clickPage(x, y);
      }
    }
  };

  // Logic for when pop ups are opened
  var onPageCreated = function(newPage) {
    if (DEBUG) console.log('New page created');
    ++featureNumOfPopups;
    ++numOfActivePopups;
    maliciousPageCrawler(newPage, website, finishCallback);
  };

  var onNavigationRequested = function(url, type, willNavigate, main) {
    if (DEBUG) console.log('Trying to navigate to: ' + url + ' from: ' +
      page.url);
    if (DEBUG) console.log('Caused by: ' + type);
    if (DEBUG) console.log('Will actually navigate: ' + willNavigate);
    if (DEBUG) console.log('Sent from the page\'s main frame: ' + main);
  };

  var onAlert = function(msg) {
    if (DEBUG) console.log('Alert msg: ' + msg);
  }

  var gridSize = 250;
  var clicksCompleted = 0;
  var clickPage = function(x, y) {
    setTimeout(function() {
      // if (DEBUG) console.log('x: ' + x + ' y: ' + y);
      clicksCompleted++;
      page.sendEvent('click', x, y);
      // Subtract 2 to account for grid sizes that are not factors of the viewport dimensions
      if (clicksCompleted >= (pageWidth * pageHeight / (gridSize *
          gridSize)) - 2) {
        setTimeout(function() {
          // Wait before finishing up on the page
          finishCallback();
        }, 10000);
      }
    }, (Math.random() * 1000));
  };

  page.onError = onError;
  page.onResourceRequested = onResourceRequested;
  page.onResourceReceived = onResourceReceived;
  page.onLoadStarted = onLoadStarted;
  page.onLoadFinished = onLoadFinished;
  page.onPageCreated = onPageCreated;
  page.onNavigationRequested = onNavigationRequested;
  page.onAlert = onAlert;
  dumpCallback(errorFile, errorJson, resFile, resJson);

  setTimeout(function() {
    // Confirm all popup-dialogs
    // Code borrowed from http://stackoverflow.com/a/34047131/1154689
    page.evaluate(function() {
      window.alert = function(msg) {
        window.callPhantom({
          alert: msg
        }); // will call page.onCallback()
        return true; // will "close the alert"
      };
    });
    // re-bind to onAlert()
    page.onCallback = function(obj) {
      // page.onAlert(obj.alert); // will trigger page.onAlert()
      ++featureNumOfAlerts;
      if (DEBUG) console.log('Alert dialog dismissed');
    };
  }, 2000);

  // Open the page, if it's the root page
  if (popupPage === null) {
    page.open(website, function(status) {
      if (status === 'success') {
        if (DEBUG) console.log('Opened ' + page.url);
      } else {
        if (DEBUG) console.log('Could not open ' + page.url);
      }
    });
  }
};

var DEBUG = false;

var fs = require('fs');
var system = require('system');

var url = system.args[1];
var rootDirectory = system.args[2];
var numOfActivePopups = 0;
var startTime = Date.now();

var errorFileArray = [];
var errorJsonArray = [];
var resFileArray = [];
var resJsonArray = [];

// Feature variables
var featureNumOfPopups = 0;
var featureNumOfAlerts = 0;
var featureTotalLoadTime = 0;
var featureAvgLoadTime = 0;
var featureNumOfResourcesRequested = 0;
var featureNumOfResourcesReceived = 0;
var featureNumOfNonWhitelistedResourcesReceived = 0;
var featureSizeOfResourcesReceived = 0;
var featureAvgSizeOfResourcesReceived = 0;
var featureSizeOfNonWhitelistedResourcesReceived = 0;
var featureAvgSizeOfNonWhitelistedResourcesReceived = 0;
var numPagesLoaded = 0; // Needed to find the average load time

// This callback is called by the different invocations of maliciousPageCrawler
// as soon as errorFile, errorJson, resFile, resJson references are created
var dumpCallback = function(errorFile, errorJson, resFile, resJson) {
  errorFileArray.push(errorFile);
  errorJsonArray.push(errorJson);
  resFileArray.push(resFile);
  resJsonArray.push(resJson);
};

// This callback is called by the different invocations of maliciousPageCrawler
// as soon as they're done crawling the page
var finishCallback = function() {
  --numOfActivePopups;
  // If there are no active popups, stop the crawler
  if (numOfActivePopups <= 0) {
    var time = Date.now() - startTime;
    console.log('Time taken to crawl ' + url + ': ' + time +
      ' ms');
    terminate();
  }
};

var terminate = function() {
  // Features
  featureAvgLoadTime = featureTotalLoadTime / numPagesLoaded;
  featureAvgSizeOfResourcesReceived = featureSizeOfResourcesReceived /
    featureNumOfResourcesReceived;
  featureAvgSizeOfNonWhitelistedResourcesReceived =
    featureSizeOfNonWhitelistedResourcesReceived /
    featureNumOfNonWhitelistedResourcesReceived;
  var featureOutput = featureNumOfPopups + ',' + featureNumOfAlerts + ',' +
    featureTotalLoadTime + ',' + featureAvgLoadTime + ',' +
    featureNumOfResourcesRequested + ',' + featureNumOfResourcesReceived +
    ',' + featureNumOfNonWhitelistedResourcesReceived + ',' +
    featureSizeOfResourcesReceived + ',' + featureAvgSizeOfResourcesReceived +
    ',' + featureSizeOfNonWhitelistedResourcesReceived + ',' +
    featureAvgSizeOfNonWhitelistedResourcesReceived;
  fs.write(rootDirectory + '/stats.csv', featureOutput, 'w');
  console.log(featureOutput);
  // Dump error and resposne JSONs
  for (var idx = 0; idx < errorFileArray.length; idx++) {
    fs.write(errorFileArray[idx], JSON.stringify(errorJsonArray[idx], 4, null),
      'w');
    fs.write(resFileArray[idx], JSON.stringify(resJsonArray[idx], 4, null),
      'w');
  }
  // Kill the crawler
  phantom.exit();
};

console.log('Beginning to crawl ' + url);
maliciousPageCrawler(null, url, finishCallback);

// 60 second timeout for the crawler
setTimeout(function() {
  console.log('Crawler is taking too long, aborting..');
  terminate();
}, 60000);
