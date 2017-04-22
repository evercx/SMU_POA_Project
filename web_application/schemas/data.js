/*****************************************************************************************************************
 Author:  刘敏杰             Date:  2016/09/20
 Description: 高校新闻数据分析表
 ********************************************************************************************************************/

var mongoose = require('mongoose');
var dataSchema = new mongoose.Schema({

    school:{     //大学名称
        type:String
    },
    study:{     //学习分类
        type:String
    },
    activity:{     //活动分类
        type:String
    },
    entrance:{     //入学分类
        type:String
    },
    social:{     //社会分类
        type:String
    }
});



module.exports = dataSchema;