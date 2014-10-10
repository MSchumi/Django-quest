$(function() {
	$("#questionBtn").bind("click",submitQuestion);
	$(".form-change").on('click',changeLogin);
});

document.onkeydown=function(event){
        var e = event || window.event || arguments.callee.caller.arguments[0];         
         if(e && e.keyCode==13){ // enter 键
          if($("#navsearch").val().replace(/(^\s+)|(\s+$)/g,"")!="")
            searchByKeyWord()
        }
    }; 

function searchByKeyWord () {
   var location=window.location
   window.location.href=location.protocol+"//"+location.host+"/question/search/?q="+encodeURIComponent($("#navsearch").val())+"&type=question";
}
var questionBlood = new Bloodhound({
  datumTokenizer: function (d) {
            return Bloodhound.tokenizers.whitespace(d.value);
        },
  queryTokenizer: Bloodhound.tokenizers.whitespace,
  remote:{
  			filter:function (response) {
  				var data=[]
  	 			if(response!=undefined){

  	 				var rows=typeof response=="object"?response:$.parseJSON(response);
  	 				for(var i=0;i<rows.length;i++){
  	 					data.push({id:rows[i]['id'],value:rows[i]['title']})
  	 				}
  	 			}
  				 return data
  			},
  			replace: function () {
            var q = '/question/searchsuggestions/?';
            if ($("#navsearch").val()) {
                q += "q=" + encodeURIComponent($("#navsearch").val());
            }
            return q;
        	},
            url: "/question/searchsuggestions/",
            ajax: {
                type: "get",
                dataType: "json",
                contentType: "application/json; charset=utf-8"
            }
        }
});
var userBlood = new Bloodhound({
 datumTokenizer: function (d) {
            return Bloodhound.tokenizers.whitespace(d.value);
        },
  queryTokenizer: Bloodhound.tokenizers.whitespace,
  remote:{
  			filter:function (response) {
  				var data=[]
          if(response!=undefined){

            var rows=typeof response=="object"?response:$.parseJSON(response);
            for(var i=0;i<rows.length;i++){
              data.push({id:rows[i]['id'],value:rows[i]['username']})
            }
          }
           return data
  			},
        replace: function () {
            var q = '/account/searchsuggestions/?';
            if ($("#navsearch").val()) {
                q += "q=" + encodeURIComponent($("#navsearch").val());
            }
            return q;
          },
            url: "/account/searchsuggestions/",
            ajax: {
                type: "get",
                dataType: "json",
                contentType: "application/json; charset=utf-8"
            }
        }
});
questionBlood.initialize();
userBlood.initialize();
$('#navsearch').typeahead({//hint: true,
        highlight: true}, [
{
  name: 'user',
  displayKey: 'value',
  source: userBlood.ttAdapter(),
  templates: {
    empty: [
      '<div class="empty-message">',
      '暂无相关用户信息',
      '</div>'
    ].join('\n'),
    header: '<h3 class="league-name">用户</h3>',
    suggestion: Handlebars.compile('<p><a href="/account/userinfo/{{id}}"><strong>{{value}}</strong></a></p>')
  }
},
  {
  name: 'question',
  displayKey: 'value',
  source: questionBlood.ttAdapter(),
  templates: {
    empty: [
      '<div class="empty-message">',
      '暂无相关问题,您可以提问获取帮助或者进一步检索',
      '</div>'
    ].join('\n'),
    header: '<h3 class="league-name">问题</h3>',
    suggestion: Handlebars.compile('<p><a href="/question/{{id}}"><strong>{{value}}</strong></a></p>')
  }
 }
]
);
function submitQuestion() {
  var title = $("#question-title").val();
  var content = $("#question-content").val();
  var category = $("#question-category").val();
  var data = {
    "title": title,
    "content": content,
    "category": category
  };
  $.ajax({
    url: "/question/submittal/",
    type: "post",
    data: data
  }).done(function(result) {
    $('#quest').modal('hide');
    location.href="/question/"+result;
  }).fail(function(xhr, status, msg) {
    alert("失败");
  }).always(function(){
    
  })
}
function changeLogin (argument) {
	var $this=$(this)
	var $parent=$this.parents(".tab-pane")
	$parent.addClass('hidden')
	$parent.siblings('').removeClass('hidden')
}