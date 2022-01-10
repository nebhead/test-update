$(document).ready(function(){
	//console.log('Enabled!')
	req = $.ajax({
		url : '/checkupdate',
		type : 'GET'
	});
	req.done(function(data) {
		if(data['result'] != 'success') {
			alert('Failed to enable API!');
		} else {
			console.log(data)
			var status_string = 'Your system is ' + data['behind'] + ' commits behind.';
			$('#update_status').html(status_string);
			$('#update_status_spinner').hide();
		};
	});
  });