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
				$('#update_checking').hide();
				$('#commits_behind').html(data['behind']);
				$('#update_available').show();
			} else {
				$('#update_checking').hide();
				$('#update_current').show();
			}
		};
	});
  });