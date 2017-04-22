/*****************************************************************************************************************
 Author:  刘敏杰             Date:  2016/09/20
 Description:  高校新闻详情表
 ********************************************************************************************************************/

var mongoose = require('mongoose');
var newsSchema = new mongoose.Schema({
    school:{     //大学名称
        type:String
    },
    classification:{   //分类名称
        type:String
    },
    title:{     //新闻标题
        type:String
    },
    url:{     //新闻地址
        type:String
    },
    date:{     //新闻发布时间
        type:String
    }
});



module.exports = newsSchema;