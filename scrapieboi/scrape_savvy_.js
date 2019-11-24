let cheerio = require('cheerio')
var request = require('request');
const fs = require('fs');

const baseurl = 'https://www.signingsavvy.com'

let words = []
let llen = 0

let check_siteOK = (data, callNext) => {
  //console.log(`checking word ${data.word}`)
  request({url: data.url, method: "HEAD"}, function (error, response, html) {
    if (!error && response.statusCode == 200) {
      words.push(data)
      //console.log(`${words.length} word-urls scraped.`)
    }else{
      console.log(`word ${data.word} has no site.`)
    }
    if(callNext){
      console.log(`scraped ${words.length - llen} new words`)
      llen = words.length
      _nextLoop()
    }
  });
}

let scrape = (letter) => {
  let url = `${baseurl}/browse/${letter}`
  request(url, function (error, response, html) {
    if (!error && response.statusCode == 200) {
      _scrape(html, url, letter)
    }
  });
}

let _scrape = (html, url, letter) => {
  let $ = cheerio.load(html)

  let items = $('div.search_results ul li a')
  items.each((index, element) => {
    let txt = $(element).text()
    let href = baseurl + "/" + $(element).attr('href')
    check_siteOK({word: txt, url: href}, index==(items.length-1))
  })
}

let i=0;

let _nextLoop = () => {
  if(i>=26) return
  let char = String.fromCharCode(i+65).toUpperCase();
  console.log(`scraping ${char}`)
  scrape(char)
  i++;

  let json = JSON.stringify(words)
  fs.writeFileSync('data.json', json)
}


_nextLoop()
