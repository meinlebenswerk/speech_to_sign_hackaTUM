let cheerio = require('cheerio')
var request = require('request');
const fs = require('fs');
var exec = require('child_process').exec;

const baseurl = 'https://www.signingsavvy.com'

let data = JSON.parse(fs.readFileSync('data_clean.json')).slice(3000)
let llen = 0

let downloadVideo = (href, item) => {
  // extract the file name
  var file_name = item.word.toLowerCase() + ".mp4"
  file_name = file_name.replace(/ /g, '_')
  file_name = file_name.replace(/\'/g, '_')
  file_name = file_name.replace(/\(/g, '_')
  file_name = file_name.replace(/\)/g, '_')
  // compose the wget command
  var wget = 'wget -P ' + "./video_data" + " -O " + file_name + ' ' + href;
  // excute wget using child_process' exec function

  var child = exec(wget, function(err, stdout, stderr) {
    if (err) throw err;
    else console.log(file_name + ' downloaded.');
  });
  _nextLoop()
}

let check_videoOK = (href, item) => {
  //console.log(`checking word ${data.word}`)
  request({url: data.url, method: "HEAD"}, function (error, response, html) {
    if (!error && response.statusCode == 200) {
      downloadVideo(href, item)
    }
  });
}

let scrape = (item) => {
  request(item.url, function (error, response, html) {
    if (!error && response.statusCode == 200) {
      _scrape(html, item)
    }
  });
}

let _scrape = (html, item) => {
  let $ = cheerio.load(html)

  let items = $('div.videocontent link')
  items.each((index, element) => {
    let href = baseurl + "/" + $(element).attr('href')
    downloadVideo(href, item)
  })
}

let i=0;

let _nextLoop = () => {
  if(i>=data.length) return
  let item = data[i]
  console.log(item)
  scrape(item)
  i++;
}


_nextLoop()
