
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
			universityTitleApp.title = this.currentUniversity;
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


var formApp = new Vue({
	el:"#formApp",
	data:{
		formInline:{
			classification:'~',
			sentiment:'~'
		}
	},
	methods: {
		onSubmit() {
			console.log('submit!');
			console.log(this.formInline);
			paginationApp.search();

		}
	}
})

var paginationApp= new Vue({
	el: '#paginationApp',
	data : {
		totalNumbers:0,
		pageSize:5,
		currentPage:1
	},
	methods:{
		handleCurrentChange(val) {
			var requestConfig = {
				method: 'get',
				url: '/api/v1/news',
				params:{
					limit:paginationApp.pageSize,
					skip:(val-1) * this.pageSize,
					sort:"-date",
					query:{
						"classification":formApp.formInline.classification,
						"sentiment":formApp.formInline.sentiment,
						"Uname":universityTitleApp.title
					}
				}
			}
			axios(requestConfig).then(function (res) {
				newsListApp.tableData = res.data;
			})
		},
		setTotalNumber(){
			var requestConfig = {
				method: 'get',
				url: '/api/v1/news/count',
				params:{
					query:{
						"classification":formApp.formInline.classification,
						"sentiment":formApp.formInline.sentiment,
						"Uname":universityTitleApp.title
					}
				}
			}
			axios(requestConfig).then(function (res) {
				paginationApp.totalNumbers = res.data.count;
			})
		},
		search(){
			paginationApp.currentPage = 1;
			this.setTotalNumber();
			this.handleCurrentChange(1);
		}
	}
});


var newsListApp = new Vue({
	el:"#newsListApp",
	data:{
		tableData:[]
	},
	methods: {
		handleEdit(index, row) {
			window.location.href = row.url;
		}
	}
})






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







