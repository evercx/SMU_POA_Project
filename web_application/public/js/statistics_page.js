
var paginationApp= new Vue({
	el: '#paginationApp',
	data : {
		totalNumbers:20,
		pageSize:5
	},
	methods:{
		handleCurrentChange(val) {
			//this.currentPage = val;
			var requestConfig = {
				method: 'get',
				url: '/api/v1/newsnumber',
				params:{
					limit:paginationApp.pageSize,
					skip:(val-1) * this.pageSize
				}
			}
			axios(requestConfig).then(function (res) {
				tableListApp.dataList = res.data;
			})
		}
	}
});

var tableListApp = new Vue({
	el:"#tableList",
	data:{
		dataList:[]
	},
	created:function() {
		var _self = this;
		var requestConfig = {
			method: 'get',
			url: '/api/v1/newsnumber',
			params:{
				limit:paginationApp.pageSize
			}
		}
		axios(requestConfig).then(function (res) {
			_self.dataList = res.data;
		})
	}
})



var option = {

	title : {
		text: '各分类下新闻所占比',
		x:'center',
		textStyle: {
			color: '#ff6600'
		}
	},
	tooltip : {
		trigger: 'item',
		formatter: "{b} : {c} ({d}%)"
	},
	legend: {
		orient: 'vertical',
		left: 'left',
		data: ['社会新闻','招生考试','社会活动','学习学术']
	},
	series : [
		{
			//name: '访问来源',
			type: 'pie',
			radius : '55%',
			center: ['50%', '60%'],
			data:[
				{value:335, name:'社会新闻'},
				{value:310, name:'招生考试'},
				{value:234, name:'社会活动'},
				{value:135, name:'学习学术'},
			],
			itemStyle: {
				emphasis: {
					shadowBlur: 10,
					shadowOffsetX: 0,
					shadowColor: 'rgba(0, 0, 0, 0.5)'
				}
			}
		}
	]
}

function getSocialCount(){
	return axios({
		method: 'get',
		url: '/api/v1/news/count',
		params:{
			query:{
				"classification":"social"
			}
		}
	})
}
function getActivityCount(){
	return axios({
		method: 'get',
		url: '/api/v1/news/count',
		params:{
			query:{
				"classification":"activity"
			}
		}
	})
}
function getEntranceCount(){
	return axios({
		method: 'get',
		url: '/api/v1/news/count',
		params:{
			"query":{
				"classification":"entrance"
			}
		}
	})
}
function getStudyCount(){
	return axios({
		method: 'get',
		url: '/api/v1/news/count',
		params:{
			query:{
				"classification":"study"
			}
		}
	})
}

var newsProportionChart = echarts.init(document.getElementById('newsProportion'),'shine');
axios.all([getSocialCount(),getActivityCount(),getEntranceCount(),getStudyCount()])
	.then(axios.spread(function(socialRes,activityRes,entranceRes,studyRes){

		newsProportionChart.setOption({
			series : [
				{
					type: 'pie',
					radius : '55%',
					center: ['50%', '60%'],
					data:[
						{value:socialRes.data.count, name:'社会新闻'},
						{value:entranceRes.data.count, name:'招生考试'},
						{value:activityRes.data.count, name:'社会活动'},
						{value:studyRes.data.count, name:'学习学术'},
					]
				}
			]
		})
	}))

newsProportionChart.setOption(option);




