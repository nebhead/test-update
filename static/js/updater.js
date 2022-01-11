$(document).ready(function(){
	//console.log('Enabled!')
	req = $.ajax({
		url : '/checkupdate',
		type : 'GET'
	});
	req.done(function(data) {
		if(data['result'] != 'success') {
			console.log(data)
			$('#update_checking').hide();
			$('#update_failed').show();
		} else {
			console.log(data)
			if(data['behind'] != 0) {
				var status_string = 'Your system is ' + data['behind'] + ' commits behind.';
				$('#update_checking').hide();
				$('#update_available').html(status_string);
				$('#update_available').show();
			} else {
				$('#update_checking').hide();
				$('#update_current').show();
			}
		};
	});
  });