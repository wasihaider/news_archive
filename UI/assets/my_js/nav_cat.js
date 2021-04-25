$(function(){
	$.ajax({
		url: "http://localhost:5000/categories",
		method: 'POST',
		contentType: 'application/json',
		dataType: 'json',
		data: JSON.stringify({}),
		success: function(response, status, type){
			console.log(response);
			populateData(response);
		}
	});

	function populateData(response){
		html = ""
		for(i=0; i<response.length;i++){
			html+='<li><a href="#" id="cat">'+response[i]+'</a></li>'
		}
		$('#cat_menu').html(html)
	}
})

$(document).on('click', "#cat", function(){
	localStorage.category = $(this).text()
	window.location.href = "pagination.html"
})