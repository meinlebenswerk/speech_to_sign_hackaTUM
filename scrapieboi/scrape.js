let cheerio = require('cheerio')
var request = require('request');
const fs = require('fs');

const baseurl = 'https://www.signasl.org'

let words = []

let check_siteOK = (data) => {
  console.log(`checking word ${data.word}`)
  request({url: data.url, method: "HEAD"}, function (error, response, html) {
    if (!error && response.statusCode == 200) {
      words.push(data)
      let json = JSON.stringify(words)
      fs.writeFileSync('data.json', json)
      console.log(`${data.length} word-urls scraped.`)
    }else{
      console.log(`word ${data.word} has no site.`)
    }
  });
}

let scrape = (letter) => {
  let url = `${baseurl}/dictionary/${letter}`
  request(url, function (error, response, html) {
    if (!error && response.statusCode == 200) {
      _scrape(html, url, letter)
    }
  });
}

let _scrape = (html, url, letter) => {
  let $ = cheerio.load(html)

  $('table tr a').each((index, element) => {
    let txt = $(element).text()
    let href = baseurl + $(element).attr('href')
    check_siteOK({word: txt, url: href})
  })
  _nextLoop()
}

let i=0;
let _nextLoop = () => {
  if(i>=26) return
  let char = String.fromCharCode(i+65).toLowerCase();
  console.log(`scraping ${char}`)
  scrape(char)
}


_nextLoop()
