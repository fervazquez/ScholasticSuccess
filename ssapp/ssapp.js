var express= require('express');
var app = express();

app.get('/',function(req,res){
    res.send("<h1><strong>HELLO B1Itches<strong><h1>");
})

app.listen(3000)