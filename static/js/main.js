$(function() {
	//$("#questionBtn").bind("click", submitQuestion);
	//$("#topicBtn").bind("click", submitTopic);
	$("#test").bind('click', test1);
	$("#question-list").on('click', '.toggle-expand', showContent);
	$("#question-list").on('click', 'a.fold-content', foldContent);

});

$(function() {
	//getHotQuestions(0);
})

function getHotQuestions(index) {
	$.ajax({
		url: '/question/hotquestions/',
		type: 'GET',
		data: {
			start: index,
			end: index + 10
		}
	})
		.done(function(data) {
			console.log("success");
			var items=$.parseJSON(data).items;
			$.each(items, function(index, val) {
				var itemDiv="<div class='question-item'><div class='question-user-info'><a><img src='/static/image/msc.jpg' class='user-photo' /></a></div><div class='question-info'><div class='title'><span class='float-right'>精品内容</span><a href='#' class='user-link'>刘东升</a><span class='bull'>&bull</span><a href='#' class='user-follow'>关注他</a></div><div class='content'><h2><a href='#'>"+val.title+"</a></h2><div class='entry-body'><div class='vote'><a href='javascript:;'>2500</a></div><div class='vote-op'><button class='up'><span class='vote-arrow'></span><span class='label'>赞同</span><span class='count'>2500</span></button><button class='down'><span class='label'>反对,不会显示你的姓名</span></button></div>"+
				"<div class='rich-text'><div class='full-content hidden'>"+val.content+"</div><div class='summary'>"+getSummary(val.content)+" <a  class='toggle-expand'>显示全部</a></div></div></div></div><div class='meta-panel'><a href='' class='question-follow'>关注问题</a><a href='#'><i></i>60条评论</a><a href=''>感谢</a><a href=''>分享</a><a  class='fold-content'>收起</a></div></div></div>";
             $("#question-list").append(itemDiv);
			});
		})
		.fail(function() {
			console.log("error");
		})
		.always(function() {
			console.log("complete");
		});
}
function getSummary(content){
	var summary=content.substring(0,200);
	if (content.length>200) {
		summary=summary+".....";

	};
    return summary;
}
function showContent(){
  var parentDiv=$(this).parent("div"); 
  var contentDiv=parentDiv.prev(".full-content").removeClass('hidden');
  parentDiv.addClass('hidden'); 
}
function foldContent(){
    var panelDiv=$(this).parent(".meta-panel").prev("div.content");
    panelDiv.find('.full-content').addClass('hidden');
    panelDiv.find('.summary').removeClass('hidden');
}
function test1() {
	$.ajax({
		url: 'question/topic/get/',
		type: 'get',
		data: {
			"keyword": "中"
		}
	})
		.done(function(data) {
			alert("success");
		})
		.fail(function(xhr, status, err) {
			alert("error");
			console.log("error");
		})
		.always(function() {
			console.log("complete");
		});



}



function submitTopic() {
	var title = $("#topic_title").val();
	var data = {
		"title": title
	};
	$.ajax({
		url: "question/topic/add/",
		type: "post",
		data: data
	}).done(function(result) {
		$('#topic').modal('hide')
	}).fail(function() {
		alert("失败");
	})
}
// 显示评论
function showcomments(){


}
