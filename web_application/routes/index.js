var express = require('express');
var path = require('path');
var router = express.Router();

/* GET home page. */
router.get('/', function(req, res, next) {
  res.sendFile(path.resolve('./','public/home.html'));
});

/* GET news page. */
router.get('/news', function(req, res, next) {
  res.sendFile(path.resolve('./','public/news.html'));
});

/* GET 404 page. */
router.get('/404', function(req, res, next) {
  res.sendFile(path.resolve('./','public/404.html'));
});


module.exports = router;
 