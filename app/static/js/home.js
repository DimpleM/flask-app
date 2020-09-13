function Delete(){

	$.ajax({
		url : '/delete',
		data : {username:$('#usernames').find('option:selected').val()},
		type : 'POST',
		success: function(res){
            res = JSON.parse(res);
			if(res.status == 1){
                alert("Successfully Deleted");
                window.location.reload();
			}
			else{
				alert("Some Error Occured");	
			}
		},
		error: function(error){
			console.log(error);
		}
    });
}

