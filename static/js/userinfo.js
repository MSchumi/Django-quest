$(function () {
	$(".user-img").bind('click', upload_img);
	$("#avat_file").bind('change', avat_change);
})

function upload_img () {
	$("#avat_file").click();
}
function avat_change (argument) {
	$(this).parent().get(0).submit();
}
function show_avatar (data) {
	$("img.user-img").attr("src",data.src);
}
 $(function() {
   $("#add").bind("click", addComment);
   $("#getAnswer").bind('click', getAnswer);
   $("button.down,button.up").on('mouseover', voteOver);
   $("button.down,button.up").on('mouseout', voteout);
   $("button.down,button.up").on('click', voteclick);
   $(".content-list").on('click','a.showComment',showComments)
   $(".content-list").on('click','.submitComment',addComment);
   $(".content-list").on('click',".vote-num",showVoter);
   $(".follow-user").on('click',followUser)
 })
function showVoter (argument) {
	var $this=$(this).parent();
  if(!$this.hasClass("no-voter")){
	$this.addClass('hidden');
	$this.prev().removeClass('hidden');
  }
}
 function voteOver() {
   var $this=$(this)
   if(!$this.hasClass('voted')){
   $this.css({
     "background-color": "#698ebf",
     "color": "#fff"
   }).children('i').css({
     "borderTopColor": "#fff",
     "borderBottomColor": "#fff"
   })
 }

 }
function voteout () {
  var $this=$(this)
  if(!$this.hasClass('voted')){
   $(this).css({
     "backgroundColor": "#eff6fa",
     "color": "#698ebf"
   }).children('i').css({
     "borderTopColor": "#698ebf",
     "borderBottomColor": "#698ebf"
   })
 }
}
function voteclick () {
  var $this=$(this)
  if($this.is(".up")){
     if($this.hasClass('voted')){
       voteAjax($this,"1","-");
       $this.removeClass('voted');
      }
      else{
      $this.next("button").removeClass('voted');
      voteAjax($this,"1","+");
      $this.addClass('voted');
    }
  }
  else{
     if($this.hasClass('voted')){
       voteAjax($this,"2","-");
       $this.removeClass('voted');
      }
      else{
      $this.prev("button").removeClass('voted');
      voteAjax($this,"2","+");
      $this.addClass('voted');
  }
  }
}
function voteAjax ($this,status,type) {
  var aid=$this.parents("div.answer-item").attr('data-token');
   $.ajax({
     url: '/question/answer/vote',
     type: 'post',
     dataType: 'text',
     data: {answerid:aid,type:type,status:status}
   })
   .done(function() {
    alert("success")
     console.log("success");
   })
   .fail(function() {
      alert("error")
     console.log("error");
   })
   .always(function() {
     console.log("complete");
   });
   
}


 function getAnswer(e) {
   e.preventDefault();
   var qid=$(".container[role=main]").attr('data-token');
   $.ajax({
     url: '/question/'+qid+'/answers',
     type: 'get',
     dataType: 'text'
   })
     .done(function(aa) {
       $(".answer-list").append(aa)
     })
     .fail(function(aa, bb, cc) {
       alert("失败")
       console.log("error");
     })
     .always(function() {
       console.log("complete");
     });

 }
function showComments(e){
  e.preventDefault();
  var $this=$(this);
  var count=parseInt($this.attr('count'));
  var $commentBox=$this.parents('div.answer-item').children('div.comment-box')
   if($commentBox.css("display")=="block"){
     $commentBox.css("display","none")
     if(count==0){
        $this.html("添加评论")
     }
     else{
        $this.html(count+"条评论")
     }
  }
  else{
    if(!$this.attr("isload")&&count>0){
       var dtd = $.Deferred();
       getComments($this,$commentBox,dtd);
       $this.attr("isload","true");
       $.when(dtd).done(function () {
              $commentBox.css("display","block")
              $this.html("收起评论")
       })

    }
    else{
    $commentBox.css("display","block")
    $this.html("收起评论")

  }
  }
}
function getComments($elem,$commentBox,dtd){
  //var qid=$(".container[role=main]").attr('data-token');
  var aid=$elem.parents("div.answer-item").attr('data-token');
  $.ajax({
    url:'/question/comment/get',
    type:'get',
    data:{"answerid":aid},
    dataType:'text'
  })
  .done(function(html){
    $commentBox.children('.comment-list').append(html)
    if(dtd!=undefined){
      dtd.resolve();
    }
  })
  .fail(function(xhr,error,status){
    alert('失败')
  })
   return dtd;
}

 function addComment(e) {
  e.preventDefault();
  var $this=$(this);
  var aid=$this.parents("div.answer-item").attr('data-token');
  var qid=$this.parents("div.answer-item").prev().attr('data-token');
  var content=$(this).parent().prev(".comment-edit-area").html();
  $.ajax({
    url:'/question/comment/add',
    type:'post',
    data:{"questionid":qid,"answerid":aid,"content":content},
    dataType:'text'
  })
  .done(function(html){
     var $commentBox=$this.parents("div.comment-edit-box").prev(".comment-list")
     $commentBox.append(html)
  })
  .fail(function(){
    alert('失败')
  })

 }

 function followUser (argument) {
   var $this=$(this)
   var uid=$(".container.user").attr("data-token");
   var tyep=1
   if($this.is(".followed")){
    $this.text("关注");
    $this.addClass('btn-success');
    $this.removeClass('btn-default followed');
    type=1;
   }
   else{
    $this.text("取消关注")
    $this.removeClass('btn-success');
    $this.addClass("btn-default followed")
    type=0
   }
   $.ajax({
    url:"/account/followuser/",
    type:"post",
    data:{"uid":uid,"type":type}
   }).done(function  (argument) {
     alert("success")
   }).fail(function  (argument) {
     alert("error")
   })
 }
 function tooltest (argument) {
  $(this).popover("show")
 }
 function test2 (argument) {
   // body...
 }