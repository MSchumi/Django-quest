$(function  (argument) {
	$("#message-tab").on('click','li',changeTab)
})

function changeTab ($e) {
	$e.preventDefault();
 	var $this=$(this);
 	$("#message-tab").find('li').removeClass('active')
 	$this.addClass('active');
   	var location=window.location;
   	window.location.href=location.protocol+"//"+location.host+"/notification/?type="+$this.attr('type');

}

$(function () {
	var messageType=$("#messagetype").val();
	$("#message-tab").find("li[type="+messageType+"]").addClass('active')
	$("#more-message").bind("click",moreMessages)
})
function moreMessages (argument) {
	$this=$("#more-message")
	var messageType=$("#messagetype").val();
	var dataCount=$this.attr("data-count")
	var endTime=$this.attr("end-time")
	$this.text("数据加载中.....")
	$.ajax({
		url:"/notification/messagelist/",
		type:"get",
		data:{"type":messageType,"skip":dataCount,"endtime":endTime}
	}).done(function (result) {
		result=$.parseJSON(result)
		if(result.count>0){
			$this.attr("data-count",parseInt(dataCount)+result.count);
			$this.attr("end-time",result.endtime);
			$("#result-list").append(result.html);
		}
		else{
			$this.remove();
		}
	}).fail(function () {
		alert("加载失败")
	}).always(function(){
		$this.text("更多")
	})
}