$(function(){


	$("#signup").click(function(){
		var first = $("#first")
		var last = $("#last")
		var email = $("#email")
		var pass = $("#pass")
		var re_pass = $("#re_pass")

		if(first.val() == ""){
			var text = "Fill required fields"
			showNotificationError('danger', null, null, null, null, null, text)
			first.css("border-color", "red")
		}
		else if(last.val() == ""){
			var text = "Fill required fields"
			showNotificationError('danger', null, null, null, null, null, text)
			last.css("border-color", "red")
		}
		else if(email.val() == ""){
			var text = "Fill required fields"
			showNotificationError('danger', null, null, null, null, null, text)
			email.css("border-color", "red")
		}
		else if(pass.val() == ""){
			var text = "Fill required fields"
			showNotificationError('danger', null, null, null, null, null, text)
			pass.css("border-color", "red")
		}
		else if(re_pass.val() == ""){
			var text = "Fill required fields"
			showNotificationError('danger', null, null, null, null, null, text)
			re_pass.css("border-color", "red")
		}

		else if(pass.val() != re_pass.val()){
			var text = "Fill required fields"
			showNotificationError('danger', null, null, null, null, null, text)
			re_pass.val("")
		}
		else {
			$.ajax({
			url: "http://localhost:5000/signup",
			method: 'POST',
			contentType: 'application/json',
			dataType: 'json',
			data: JSON.stringify({
				first_name: first.val(),
				last_name: last.val(),
				username: email.val(),
				password: pass.val()
			}),
			success: function(response, status, type){
				window.location.replace("Login.html")
			}
		});
		}
	})

	$("#register-form").submit(function(e) {
	    e.preventDefault();
	});
})