$(function  (argument) {
	$("#search-tab").on('click','li',search)
})

function search ($e) {
	$e.preventDefault();
 	var $this=$(this);
 	$("#search-tab").find('li').removeClass('active')
 	$this.addClass('active');
   	var location=window.location;
   	window.location.href=location.protocol+"//"+location.host+"/question/search/?q="+$("#searchword").val()+"&type="+$this.attr('type');

}

$(function () {
	var searchType=$("#searchtype").val();
	$("#search-tab").find("li[type="+searchType+"]").addClass('active')
})