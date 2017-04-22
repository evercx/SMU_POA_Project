var mongodb=require('./bookdb');



 mongodb.open(function(error,db){
     if(error) throw error ;
     db.collection("Novel",{
         safe : true
     },function(err,collection){
         if(err) throw err ;
         collection.find().toArray(function(e,docs){
             if(e) throw e ;
             console.log(docs) ;
         }) ; 
     }) ;
 }) ;