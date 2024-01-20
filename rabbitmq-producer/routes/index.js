// var express = require('express');
// var router = express.Router();

/* GET home page. */
// router.get('/', function(req, res, next) {
//   res.render('index', { title: 'Express' });
// });

const express = require("express");

const app = express.Router();

app.use(express.urlencoded());

app.get("/", function (request, response, next) {
  response.send(`
    <form action="/message" method="post" >
                  <div className="input">
                  <input type="text" name="message" />
                 
                  <input type="submit" value="send" />
               
              </div>
            </form>
            `);
});

app.post("/", function (request, response, next) {
  response.send(request.body);
});

// app.listen(2000);

module.exports = app;
