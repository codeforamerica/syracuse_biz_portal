'use strict';

$(document).ready(function(){
  $('.checklist-form').click(function(e){
    var formSubmitAction = $(this).attr('action');
    var formData = $(this).serialize();
    $('.checklist-status').fadeOut(200);
    $('#checklist-saving').fadeIn(200);
    $.ajax({
        type: "POST",
        url: formSubmitAction,
        data: formData,
        dataType: "json",
        success: function(data) {
            $('#checklist-saving').fadeOut(200, function(){
              $('#checklist-updated').fadeIn(200);
            });
            console.log('success')
        },
        error: function() {
            $('#checklist-saving').fadeOut(200, function(){
              $('#checklist-failed').fadeIn(200);
              $('#checklist-login-prompt').fadeIn(200);
            });
            console.error('error handing here');
        }
    });
  });
});
