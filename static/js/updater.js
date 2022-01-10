$(document).ready(function(){
	//console.log('Enabled!')
	req = $.ajax({
		url : '/checkupdate',
		type : 'GET'
	});
	req.done(function(data) {
		if(data['result'] != 'success') {
			console.log(data)
			var status_string = '<b style="color:red;">Update check failed.</b>';
			$('#update_status').html(status_string);
			$('#update_status_spinner').hide();
		} else {
			console.log(data)
			var status_string = 'Your system is ' + data['behind'] + ' commits behind.';
			$('#update_status').html(status_string);
			$('#update_status_spinner').hide();
		};
	});
  });