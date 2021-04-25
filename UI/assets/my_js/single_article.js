$(function(){
	if (localStorage.username == null){
		localStorage.username = ""
	}

	$("#commentForm").submit(function(e) {
	    e.preventDefault();
	});

	$.ajax({
		url: "http://localhost:5000/article",
		method: 'POST',
		contentType: 'application/json',
		dataType: 'json',
		data: JSON.stringify({
			'id': localStorage.doc_id,
			'username': localStorage.username
		}),
		success: function(response, status, type){
			populateData(response)
		}
	});

	$.ajax({
		url: "http://localhost:5000/get/comment",
		method: 'POST',
		contentType: 'application/json',
		dataType: 'json',
		data: JSON.stringify({
			'doc_id': localStorage.doc_id
		}),
		success: function(response, status, type){
			loadComments(response)
		}
	});

	function populateData(response){
		$("#title").html(response.title)
		if (response.image_src == null){
			$(".img-fluid").attr('src', "./assets/img/blog/alternative.jpg")
		}
		else {
			$(".img-fluid").attr('src', response.image_src)
		}
		
		// $(".img-fluid").attr('alt', )
		var options = { 
			weekday: 'long', 
			year: 'numeric', 
			month: 'long', 
			day: 'numeric' 
		};
		var date = new Date(response.date * 1000)
		var dt = date.toLocaleString("en-US", options)
		$("#date").html('<i class="fas fa-calendar"></i> '+dt)
		$("#category").html('<i class="fas fa-tag"></i> '+response.category)
		$(".excert").text(response.content)
	}

	function loadComments(response){
		html = "<h4>"+response.length+" Comments</h4>"
		for ( var i = 0, l = response.length; i < l; i++ ) {
			var options = { 
				weekday: 'long', 
				year: 'numeric', 
				month: 'long', 
				day: 'numeric',
				hour: 'numeric',
				minute: 'numeric' 
			};
			var date = new Date(response[i].time * 1000)
			var dt = date.toLocaleString("en-US", options)
		    html += '<div class="comment-list">'+
				'<div class="single-comment justify-content-between d-flex">'+
		    	'<div class="user justify-content-between d-flex">'+
		       	'<div class="thumb">'+
		          '<img src="assets/img/comment/user.png" alt="">'+
		     	'</div>'+
		       	'<div class="desc">'+
		          '<p class="comment">'+response[i].comment+'</p>'+
		         '<div class="d-flex justify-content-between">'+
		             '<div class="d-flex align-items-center">'+
		                '<h5>'+
		                   '<a href="#">'+response[i].full_name+'</a>'+
		                '</h5>'+
		                '<p class="date">'+dt+'</p>'+
		             '</div>'+
		             '</div></div></div></div></div>'
		}
		
		$(".comments-area").html(html)
	}

	// $(".comment-form").submit(function(e) {
	//     e.preventDefault();
	// });

	$("#add_comment").click(function(){
		console.log("Adding comment")
		if($("#user_email").val()==""){
			var text = "Email is required!!"
			showNotificationError('danger', null, null, null, null, null, text)
		}
		else if($("#comment_content").val() == ""){
			var text = "Please enter some input!!"
			showNotificationError('danger', null, null, null, null, null, text)
		}

		else{
			addComment($("#user_email").val(), $("#comment_content").val())
			$("#comment_content").val('');
			$("#user_email").val('');
			$.ajax({
				url: "http://localhost:5000/get/comment",
				method: 'POST',
				contentType: 'application/json',
				dataType: 'json',
				data: JSON.stringify({
					'doc_id': localStorage.doc_id
				}),
				success: function(response, status, type){
					loadComments(response)
				}
			});
		}
	});

	function addComment(username, comment){
		$.ajax({
			url: "http://localhost:5000/add/comment",
			method: 'POST',
			contentType: 'application/json',
			dataType: 'json',
			data: JSON.stringify({
				doc_id: localStorage.doc_id,
				username: username,
				comment: comment
			}),
			success: function(response, status, type){
				var text = "Message sent!!"
				showNotificationError('success', null, null, null, null, null, text)
			}
		});
	}
})

$(document).on('click', "#search", function(e){
	localStorage.query = $("#query").val();
	window.location.replace("categori.html")
})
