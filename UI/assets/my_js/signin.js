$(function() {
	$("#signin").click(function(){
		var email = $("#email")
		var pass = $("#pass")

		if(email.val() == ""){
			var text = "Fill required fields"
			showNotificationError('danger', null, null, null, null, null, text)
			email.css("border-color", "red")
		}
		else if(pass.val() == ""){
			var text = "Fill required fields"
			showNotificationError('danger', null, null, null, null, null, text)
			pass.css("border-color", "red")
		}
		else {
			$.ajax({
			url: "http://localhost:5000/signin",
			method: 'POST',
			contentType: 'application/json',
			dataType: 'json',
			data: JSON.stringify({
				username: email.val(),
				password: pass.val()
			}),
			success: function(response, status, type){
				console.log(response)
				console.log(response.success)
				if (response.success == true){
					localStorage.username = email.val();
					window.location.replace("index.html");
				}
				else{
					alert('Invalid username or password')
				}
			},
		});
		}
	})
	$("#login-form").submit(function(e) {
	    e.preventDefault();
	});
})