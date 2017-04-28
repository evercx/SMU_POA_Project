
var sideListApp = new Vue({
	el:"#sideBar",
	data:{
		universityList:[
			{
				name: "上海海事大学",
				isActive: true
			},

			{
				name: "上海交通大学",
				isActive: false
			},

			{
				name: "同济大学",
				isActive: false
			},

			{
				name: "复旦大学",
				isActive: false
			},

			{
				name: "华东师范大学",
				isActive: false
			},

			{
				name: "上海大学",
				isActive: false
			},

			{
				name: "华东理工大学",
				isActive: false
			},

			{
				name: "东华大学",
				isActive: false
			},

			{
				name: "上海财经大学",
				isActive: false
			},

			{
				name: "上海外国语大学",
				isActive: false
			},

			{
				name: "华东政法大学",
				isActive: false
			},

			{
				name: "上海师范大学",
				isActive: false
			},

			{
				name: "上海理工大学",
				isActive: false
			},

			{
				name: "上海海洋大学",
				isActive: false
			},

			{
				name: "上海中医药大学",
				isActive: false
			},

			{
				name: "上海音乐学院",
				isActive: false
			},

			{
				name: "上海戏剧学院",
				isActive: false
			},

			{
				name: "上海对外经贸大学",
				isActive: false
			},

			{
				name: "上海电机学院",
				isActive: false
			},

			{
				name: "上海工程技术大学",
				isActive: false
			}
		],
		currentUniversity:"上海海事大学"
	},
	methods:{
		selectUniversity:function(universityName){
			changeActiveStatusByUniversityName(this.universityList,universityName,true);
			this.currentUniversity = universityName;
			universityTitleApp.title = universityName;
			universityTitleApp.updateSubtitle(universityTitleApp.title)
		}
	},
	computed:{

	}
});


var universityTitleApp =new Vue({
	el:"#universityTitle",
	data:{
		title:sideListApp.currentUniversity,
		subtitle:''

	},
	created:function(){
		var _self = this;
		axios({
			method: 'get',
			url: '/api/v1/news/count',
			params:{
				query:{
					"Uname":_self.title
				}
			}
		}).then(function(res){
			_self.subtitle = "当前系统中共有"+res.data.count+"条新闻数据......";
		})
	},
	computed:{},
	methods:{
		updateSubtitle:function(universityName){
			var _self = this;
			axios({
				method: 'get',
				url: '/api/v1/news/count',
				params:{
					query:{
						"Uname":universityName
					}
				}
			}).then(function(res){
				_self.subtitle = "当前系统中共有"+res.data.count+"条新闻数据......";
			})
		}
	},
})

// function findCurrentUniversity(){
// 	for (i in sideListApp.universityList){
// 		if (sideListApp.universityList[i].status) return sideListApp.universityList[i].name;
// 		return '上海海事大学';
// 	}
// }

function changeActiveStatusByUniversityName(list,name,status){

	if(status){
		for(i in list){
			if(list[i].isActive === true){
				list[i].isActive = false
			}
		}
		for(i in list){

			if(list[i].name === name){
				console.log(list[i])
				list[i].isActive = status
				console.log(list[i])
			}
		}
	}
}







