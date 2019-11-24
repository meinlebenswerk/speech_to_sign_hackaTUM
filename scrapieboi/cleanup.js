const fs = require('fs');

let data = JSON.parse(fs.readFileSync('data.json'))
let new_data = []

let inNewData = (element) => {
  for(let i=0; i<new_data.length; i++){
    let ndel = new_data[i]
    if(ndel.word == element.word) return true
  }

  return false
}

for(let i=0; i<data.length; i++){
  let el = data[i]
  if(!inNewData(el)){
    new_data.push(el)
  }
}

console.log(data.length)
console.log(new_data.length)

let out = JSON.stringify(new_data)
fs.writeFileSync('data_clean.json', out)
