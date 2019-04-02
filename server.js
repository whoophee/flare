'use strict';
const WebSocket = require('ws')
const fs = require('fs')
const wss = new WebSocket.Server({ port: 9001 })
wss.on('connection', function connection(ws) {
   let msgarray1 = [];
   let msgarray2 = [];
   let msgarray3 = [];
   let msgarray4 = [];
   let msgarray5 = [];
   let msgarray6 = [];
   let msgarray7 = [];
   let msgarray8 = [];
   let msgarray9 = [];
   let msgarray10 = [];
   const track_hero = (filename, array, i) => {
       var lineReader = require('readline').createInterface({
         input: require('fs').createReadStream("replays/chong/"+filename)
       });
       lineReader.on('line', function (line) {
           array.push(i+" "+line)
       });
   };
   const read_array = (array) => {
       if (array.length>0) {
           let pack = array.shift()
           ws.send(pack)
       }
   };
   track_hero("Juggernaut.txt", msgarray1,"1")
   track_hero("Nevermore.txt", msgarray2,"2")
   track_hero("Winter_Wyvern.txt", msgarray3,"3")
   track_hero("Tiny.txt", msgarray4,"4")
   track_hero("Tusk.txt", msgarray5,"5")
   track_hero("Grimstroke.txt", msgarray6,"6")
   track_hero("Furion.txt", msgarray7,"7")
   track_hero("Morphling.txt", msgarray8,"8")
   track_hero("Shredder.txt", msgarray9,"9")
   track_hero("EarthSpirit.txt", msgarray10,"10")
   setInterval(()=> {
      read_array(msgarray1)
      read_array(msgarray2)
      read_array(msgarray3)
      read_array(msgarray4)
      read_array(msgarray5)
      read_array(msgarray6)
      read_array(msgarray7)
      read_array(msgarray8)
      read_array(msgarray9)
      read_array(msgarray10)
  }, 32);
});
