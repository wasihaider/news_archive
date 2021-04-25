$(function(){
	localStorage.page = 1
	console.log(localStorage.query)
	call_api();
	function call_api(){
		$.ajax({
		url: "http://localhost:5000/search/query",
		method: 'POST',
		contentType: 'application/json',
		dataType: 'json',
		data: JSON.stringify({
			'query': localStorage.query,
			'page': localStorage.page,
			'category': localStorage.query_category,
			'start_date': localStorage.start_date,
			'end_date': localStorage.end_date
		}),
		success: function(response, status, type){
			console.log(response);
			populateData(response.docs.articles);
			paginate(response.docs.page, response.docs.total);
			generate_wordcloud(response.wordcloud)
		}
	});
	}
	

	function populateData(response){
		$("#query").val(localStorage.query)
		html = "<br><br>"
		if(response.length==0){
			html += '<h1 class="text-secondary">No data found</h1>';
			console.log(html)
			$("#results").html(html);
			return;
		}
		for(var i=0; i<response.length;i++){
			if(response[i].image_src == null){
				response[i].image_src = "./assets/img/blog/alternative.jpg"
			}
			var options = { 
				weekday: 'long', 
				year: 'numeric', 
				month: 'long', 
				day: 'numeric' 
			};
			var date = new Date(response[i].date * 1000)
			var dt = date.toLocaleString("en-US", options)
			var category = response[i].category
			html += '<div class="trand-right-single d-flex">'+
                '<div class="trand-right-img">'+
                    '<img src="'+response[i].image_src+'" alt="">'+
                '</div>'+
                '<div class="trand-right-cap">'+
                
                    '<h4><a href="single-blog.html" id="art" data-id="'+response[i].doc_id+'">'+response[i].title+'</a></h4>'+
                	'<ul class="blog-info-link mt-3 mb-4">'+
                        '<li><a id="date"><i class="fas fa-calendar"></i> '+dt+'</a></li>'+
                        '<li><a id="category"><i class="fas fa-tag"></i> '+category+'</a></li>'+
                     '</ul>'+
                '</div></div>'
		}
		$("#results").html(html);
	}

	function paginate(page, total){
		first = '<li class="page-item"><a class="page-link" id="prev" ><span class="flaticon-arrow roted right-arrow"></span></a></li>';
		last = '<li class="page-item"><a class="page-link" id="next" ><span class="flaticon-arrow right-arrow"></span></a></li>';
		var center = "";
		if(total==0){
			return;
		}
		if(page == 1){
			first = '<li class="page-item"><a class="page-link" id="page"><span class="flaticon-arrow roted"></span></a></li>';          
		}
		if(page == total){
			last = '<li class="page-item"><a class="page-link" id="page"><span class="flaticon-arrow"></span></a></li>';
		}
		if(total < 8){
			for(i=1; i<=total; i++){
				var element = '<li class="page-item"><a class="page-link" id="page">'+i+'</a></li>';
				if(i==page){
					element = '<li class="page-item active"><a class="page-link" id="page">'+i+'</a></li>';
				}
				center+=element;
			}
		}
		else if(page < 5){
			for(i=1; i<=5; i++){
				var element = '<li class="page-item"><a class="page-link" id="page">'+i+'</a></li>';
				if(i==page){
					element = '<li class="page-item active"><a class="page-link" id="page">'+i+'</a></li>';
				}
				center+=element;
			}
			center+='<li class="page-item"><a class="page-link" style="pointer-events: none">...</a></li>';
			center+='<li class="page-item"><a class="page-link" id="page">'+total+'</a></li>';
		}
		else if(page >= (total-3)){
			center+='<li class="page-item"><a class="page-link" id="page">1</a></li>';
			center+='<li class="page-item"><a class="page-link" style="pointer-events: none">...</a></li>';
			for(i=total-3; i<=total; i++){
				var element = '<li class="page-item"><a class="page-link" id="page">'+i+'</a></li>';
				if(i==page){
					element = '<li class="page-item active"><a class="page-link" id="page">'+i+'</a></li>';
				}
				center+=element;
			}
		}
		else{
			center+='<li class="page-item"><a class="page-link" id="page">1</a></li>';
			center+='<li class="page-item"><a class="page-link" style="pointer-events: none">...</a></li>';
			// console.log(page)
			// console.log()
			for(i=page; i<=+(page)+2; i++){
				// console.log(i)
				var element = '<li class="page-item"><a class="page-link" id="page">'+i+'</a></li>';
				if(i==page){
					element = '<li class="page-item active"><a class="page-link" id="page">'+i+'</a></li>';
				}
				center+=element;
			}
			center+='<li class="page-item"><a class="page-link" style="pointer-events: none">...</a></li>';
			center+='<li class="page-item"><a class="page-link" id="page">'+total+'</a></li>';
		}

		html = first+center+last;
		$(".pagination").html(html);
	}


$(document).on('click', "#art", function(e){
	// alert($(this).attr('data-id'));
	localStorage.doc_id = $(this).attr("data-id")
})

$(document).on('click', "#search", function(e){
	var query = $("#query").val();
	if (query == ""){
		// alert("Enter some search term!")
		var text = "Enter some search term"
		showNotificationError('danger', null, null, null, null, null, text)
	}
	else{
		localStorage.query = $("#query").val();
		window.location.replace("categori.html")
	}
})

$(document).on('click', '#prev', function(){
	var page = Number(localStorage.page)-1;
	if (localStorage.page != page){
		localStorage.page = page;
		call_api();
	}
})

$(document).on('click', '#next', function(){
	var page = Number(localStorage.page)+1;

	if (localStorage.page != page){
		localStorage.page = page;
		call_api();
	}
})

$(document).on('click', '#page', function(){
	var page = Number($(this).text())
	// alert(page)
	if (localStorage.page != page){
		localStorage.page = page;
		call_api();
	}
})

$( window ).unload(function(){
	localStorage.query_category = null;
	localStorage.start_date = null;
	localStorage.end_date = null;
})

function generate_wordcloud(data) {
	Highcharts.chart('container', {
		chart : {
			type: "wordcloud"
		},
	    accessibility: {
	        screenReaderSection: {
	            beforeChartFormat: '<h5>{chartTitle}</h5>' +
	                '<div>{chartSubtitle}</div>' +
	                '<div>{chartLongdesc}</div>' +
	                '<div>{viewTableButton}</div>'
	        }
	    },
	        plotOptions: {
	        series: {
	            cursor: 'pointer',
	            point: {
	            	events: {
	                click: function (event) {
	                    append_search(this.name)
	                }
	            }
	            }
	            
	        }
	    },
	    series: [{
	        // type: 'wordcloud',
	        data: data,
	        // name: 'Occurrences'
	    }],
	    title: {
	        text: 'Wordcloud of queries'
	    },
	    tooltip: {
	        headerFormat: '<b>{point.name}</b><br/>',
	        pointFormat: 'frequency: {point.weight}'
	    },
	});
}


function append_search(word) {
	console.log("here")
	var query = $("#query");
	input = query.val();
	if(input == ""){
		input = word
	}
	else{
		input = input + " " + word
	}
	query.val(input)
	console.log(input)
}
})

