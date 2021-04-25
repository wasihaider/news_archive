$(function(){
	$.ajax({
		url: "http://localhost:5000/most/recent/articles",
		method: 'POST',
		contentType: 'application/json',
		dataType: 'json',
		data: JSON.stringify({
			'username': localStorage.username
		}),
		success: function(response, status, type){
			populateData(response)
		}
	});

	function populateData(response){
		console.log(response)
		
		if (response[0].image_src == null){
			response[0].image_src = "./assets/img/blog/alternative.jpg"
		}
		$("#top_image").attr('src', response[0].image_src)
		$("#top_title").text(response[0].title)
		$("#top_title").attr('data-id', response[0]._id)
		html = ""

		for (var i=1; i<7; i++){
			if (response[i].image_src == null){
				response[i].image_src = "./assets/img/blog/alternative.jpg"
			}
			html += '<div class="trand-right-single d-flex">'+
            '<div class="trand-right-img">'+
            '<img src="'+response[i].image_src+'" alt="">'+
                            '</div>'+
                            '<div class="trand-right-cap">'+
                                '<h4 id="title"><a href="single-blog.html" data-id="'+response[i]._id+'" id="top_title">'+response[i].title+'</a></h4>'+
                            '</div></div>'

		}
		$("#right_arts").html(html)
		bottom = ""
		for (var i=7; i<response.length; i++){
			if (response[i].image_src == null){
				response[i].image_src = "./assets/img/blog/alternative.jpg"
			}
			bottom += '<div class="col-lg-4">'+
                '<div class="single-bottom mb-35">'+
                    '<div class="trend-bottom-img mb-30">'+
                        '<img src="'+response[i].image_src+'" alt="">'+
                    '</div>'+
                    '<div class="trend-bottom-cap">'+
                        
                        '<h4></h4><h4 id="title"><a href="single-blog.html" id="top_title" data-id="'+response[i]._id+'">'+response[i].title+'</a></h4>'+
                    '</div></div></div>'
		}
		$("#bottom_arts").html(bottom)
	};

	// $("#art").click(function(){
	// 	alert("here");
	// 	alert($(this).attr('data-id'));
	// })

	function search(){
		var query = $("#query").val();
		if (query == ""){
			alert("Enter some search term!")
		}
		else{
			console.log("going to search")
			localStorage.query = $("#query").val();
			// window.location.replace("categori.html");
			window.location = "categori.html"
		}
	}

$(document).on('click','#top_title',function(e) {
  localStorage.doc_id = $(this).attr('data-id');
});

$(document).on('click','#search', function(){
	search()	
})
var wage = document.getElementById("query");
wage.addEventListener("keydown", function (e) {
	
    if (e.keyCode === 13) {  //checks whether the pressed key is "Enter"
        console.log("Enter pressed")
        search();
    }
});


})