var express = require('express');
var router = express.Router();
var mongodb=require('../dao/poadb')
router.post('/',function(req,res,next){
    console.log(req.body);
    school=req.body.school;
    mongodb.open(function(error,db){
     if(error) throw error ;
     db.collection('data').find({"school":school}).toArray(function (e,docs) {
        db.close();
        res.send(docs);
     });

    //  db.collection('data',{safe : true},function(err,collection){
    //      if(err) {console.log('col error');throw err };
    //      collection.find({"school":school}).toArray(function(e,docs){
    //          if(e) {console.log('find error');throw e ;}
    //          console.log(docs);
    //          res.setHeader("Access-Control-Allow-Origin", "*");
    //          res.send(docs)
    //      }) ;
    //  }) ;
    }) ;

})

module.exports = router;
