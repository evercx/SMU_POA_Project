var express = require('express');
var path = require('path');
var router = express.Router();
var mongoose = require('mongoose');
var restify = require('express-restify-mongoose');
var ipConfig = require('../ipConfig');

var collegesModel = require('../models/colleges');
var dataModel = require('../models/data');
var newsModel = require('../models/news');

mongoose.connect(ipConfig.mongodb);

//接口过滤中间件,只允许GET操作,防止对数据库的修改操作
router.use('/api/v1/*',function(req,res,next){
    if(req.method !== 'GET'){
      console.log("\n\n当前操作不是get,其操作为: "+req.method);
      res.send({msg:"无权限对数据进行修改操作"});
    }else{
        console.log(req.method);
      next();
    }
 });

restify.serve(router,collegesModel);
restify.serve(router,dataModel);
restify.serve(router,newsModel);

module.exports = router;
