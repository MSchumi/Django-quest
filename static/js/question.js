 $(function() {
   $("#add").bind("click", addComment);
   $("#subAnswer").bind('click', addAnswer);
   $("#getAnswer").bind('click', getAnswer);
   $("button.down,button.up").on('mouseover', voteOver);
   $("button.down,button.up").on('mouseout', voteout);
   $("button.down,button.up").on('click', voteclick);
   $(".answer-list").on('click','a.showComment',showComments)
   $(".answer-list").on('click','.submitComment',addComment);
   $(".follow-question").on('click',followQuestion)
   $(".answer-list").on('click','a.replay_comment',replayComment)
   validateLogin($(".answer-edit-box"));
 })

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
 function followQuestion (argument) {
   var $this=$(this)
   var qid=$(".container[role=main]").attr('data-token');
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
    url:"/question/follow/",
    type:"post",
    data:{"qid":qid,"type":type}
   }).done(function  (argument) {
     alert("success")
   }).fail(function  (argument) {
     alert("error")
   })
 }
function voteout (e,$obj) {
  var $this=$(this)
  if($obj&&$obj.is("button")){
    $this=$obj;
  }
  if(!$this.hasClass('voted')){
    $this.css({
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
       var $count=$this.parents(".votebar");
       var vote_count=parseInt($count.attr("vote"))
       $count.attr('vote',vote_count-1);
       var count=$this.children(".vote-count").text(vote_count-1);
      }
      else{
    
      if($this.next("button").hasClass('voted')){
          $this.next("button").removeClass('voted');
           voteout(undefined,$this.next("button"));
      }
      voteAjax($this,"1","+");
      $this.addClass('voted');
       var $count=$this.parents(".votebar");
       var vote_count=parseInt($count.attr("vote"))
       $count.attr('vote',vote_count+1);
       var count=$this.children('.vote-count').text(vote_count+1);
    }
  }
  else{
     if($this.hasClass('voted')){
       voteAjax($this,"2","-");
       $this.removeClass('voted');
      }
      else{
      if($this.siblings('').hasClass('voted')){
      var $count=$this.parents(".votebar");
       var vote_count=parseInt($count.attr("vote"))
       $count.attr('vote',vote_count-1);
       var count=$this.siblings('').children(".vote-count").text(vote_count-1);
      }
      $this.prev("button").removeClass('voted');
      voteout(undefined,$this.prev("button"));
      voteAjax($this,"2","+");
      $this.addClass('voted');
  }
  }
}
function voteAjax ($this,status,type) {
  var aid=$this.parents("div.answer-item").attr('data-token');
  var eid=$this.parents("div.answer-item").attr('eid');
  var data={answerid:aid,type:type,status:status};
  if(eid!=undefined&&eid!=""){
    data.evaluation_id=eid;
  }
   $.ajax({
     url: '/question/answer/vote',
     type: 'post',
     dataType: 'text',
     data: data
   })
   .done(function(msg) {
   // alert("success")
   // console.log("success");
   if (type=="-"){
    $this.parents("div.answer-item").removeAttr("eid")
   }
   else{
    var json=$.parseJSON(msg);
    if(json.evaluation_id!=undefined){
      $this.parents("div.answer-item").attr('eid',json.evaluation_id)
    }
   }
   })
   .fail(function(aa,bb,cc) {
      alert("error")
     console.log("error");
   })
   .always(function() {
    console.log("complete");
   });
   
}
 function addAnswer() {
   var content = $("#editor").html();
   var question_id = $(".container[role=main]").attr("data-token");
   alert(question_id);
   $.ajax({
     url: 'answer/add',
     type: 'post',
     dataType: 'text ',
     data: {
       content: content,
       questionid: question_id
     }
   })
     .done(function(html) {
       $(".answer-list").append(html);
       var answerNum=$(".answer-num").html();
       $(".answer-num").html(parseInt(answerNum)+1);
       alert("添加成功")
     })
     .fail(function(aa, bb, cc) {
       alert("失败")
       console.log("error");
     })
     .always(function() {
       console.log("complete");
     });


 }
 function validateLogin ($elem) {
   if(isAnonymous()){
    var height=$elem.height();
    var width=$elem.width();
    $elem.prepend("<div class='mask' style='position:absolute;width:"+width+"px;height:"+height+"px;z-index:100;'></div>")
    $elem.bind('mousedown',function(){
      alert("请登录");
    });
   }
}
function isAnonymous () {
   if($("#loginuser").length>0){
      return false;
    }
    return true;
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
              validateLogin($this.parents('div.answer-item').children('div.comment-box'))
              $commentBox.css("display","block")
              $this.html("收起评论")
       })

    }
    else{
    $commentBox.css("display","block")
    $this.html("收起评论")
    if($commentBox.children('.mask').length==0){
      validateLogin($this.parents('div.answer-item').children('div.comment-box'))
    }
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
function replayComment (e) {
  e.preventDefault();
  var $this=$(this);
  var $parent=$this.parents(".comment-content-foot");
  var $input=$parent.find(".mment-edit-box-append");
  if($input.length>0){
    $input.remove();
  }
  else{
    var div="<div class='mment-edit-box-append'><div class='comment-edit-area' contenteditable='true'></div><div class='comment-action-area comment-append-action'><a class='command-cancel'>取消</a> <a href='#' class='btn btn-primary btn-sm submitComment replay' role='button'>提交</a></div></div>"
    $(this).parents(".comment-content-foot").append($(div))
  }
}

 function addComment(e) {
  alert()
  e.preventDefault();
  var $this=$(this);
  var qid=$(".container[role=main]").attr('data-token');
  var aid=$this.parents("div.answer-item").attr('data-token');

  var toid=$this.parents("div.answer-item").children('.answer-head').attr('data-token');
  var content=$(this).parent().prev(".comment-edit-area").html();
  if($this.is(".replay"))
  {
    toid=$this.parents(".comment-item").attr("user-token")
  }
  $.ajax({
    url:'/question/comment/add',
    type:'post',
    data:{"questionid":qid,"answerid":aid,"content":content,"touser":toid},
    dataType:'text'
  })
  .done(function(html){
     var $commentBox=$this.parents("div.comment-edit-box").prev(".comment-list")
     if($this.is(".replay")){
      var $commentBox=$this.parents(".comment-list")
      $this.parents(".comment-content-foot").find(".mment-edit-box-append").remove()
     }
     
     $commentBox.append(html)
  })
  .fail(function(){
    alert('失败')
  })

 }
 $(function() {
   function initToolbarBootstrapBindings() {
     var fonts = ['Serif', 'Sans', 'Arial', 'Arial Black', 'Courier',
         'Courier New', 'Comic Sans MS', 'Helvetica', 'Impact ', 'Lucida Grande ', 'Lucida Sans', 'Tahoma', 'Times',
         'Times New Roman', 'Verdana'
       ],
       fontTarget = $('[title = Font]').siblings('.dropdown-menu');
     $.each(fonts, function(idx, fontName) {
       fontTarget.append($('<li><a data-edit ="fontName' + fontName + '"style ="font-family:\'' + fontName + '\'"> ' + fontName + ' </a></li>'));
     });
     $('a[title]').tooltip({
       container: 'body'
     });
     $('.dropdown-menu input').click(function() {
       return false;
     })
       .change(function() {
         $(this).parent('.dropdown-menu').siblings('.dropdown-toggle').dropdown('toggle');
       })
       .keydown('esc ', function() {
         this.value = '';
         $(this).change();
       });
     $('[data-role = magic-overlay]').each(function() {
       var overlay = $(this),
         target = $(overlay.data('target'));
       overlay.css('opacity ', 0).css('position', 'absolute').offset(target.offset()).width(target.outerWidth()).height(target.outerHeight());
     });
     if ("onwebkitspeechchange" in document.createElement("input")) {
       var editorOffset = $('#editor').offset();
       $('#voiceBtn').css('position', 'absolute').offset({
         top: editorOffset.top,
         left: editorOffset.left + $('#editor').innerWidth() - 35
       });
     } else {
       $('#voiceBtn').hide();
     }
   };
   function showErrorAlert(reason, detail) {
     var msg = '';
     if (reason === 'unsupported-file-type') {
       msg = "Unsupported format " + detail;
     } else {
       console.log("error uploading file", reason, detail);
     }
     $(' <div class="alert" > <button type = "button"class = "close"data - dismiss = "alert" > &times; </button>' +
       '<strong>File upload error</strong > ' + msg + ' </div>').prependTo('#alerts');
   };
   initToolbarBootstrapBindings();
   $('#editor').wysiwyg({
     fileUploadError: showErrorAlert
   });
   window.prettyPrint && prettyPrint();
 });