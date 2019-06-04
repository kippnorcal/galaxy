$('.feedback-btn').click(function(){
  $('.sentiment-icon').removeClass('fas').addClass('far');
  commentLabel = $('label[for="comments"]');
  commentLabel.show();
  $('#comments').show();
  $(this).find('i.far').removeClass('far').addClass('fas');
  score = $(this).find('[name="score"]').val();
  if(score > 3){
    commentLabel.text("What do you like about this report?");
  } else if(score < 3){
    commentLabel.text("How could this report be better?");
  } else {
    commentLabel.text("Optional comments:");
  }
});


$('#feedbackform').submit(function(event){
  event.preventDefault();
  $.ajax({
    data: $(this).serialize(),
    type: $(this).attr('method'),
    url: $(this).attr('action'),
    success: function(response){
      if(response['success']){
        $('#feedbackform')[0].reset();
        $('.feedback-btn').removeClass('text-success text-danger text-warning');
        $('.alert').prepend("<strong>Success</strong> Thanks for giving your feedback!");
        $('.alert').toggleClass('alert-info');
        $('.alert').removeAttr('hidden');
        $('.collapse').collapse('hide');
        $('.fa-comment').removeClass('far').addClass('fas');
        $('.score-badge').text(response['score']);
        $('.score-badge').removeAttr('hidden');
        $('.avg-feedback').text(response['avg_feedback']);
      }
      if(response['error']){
        $('.alert').prepend("<strong>Error</strong> Something went wrong.");
        $('.alert').toggleClass('alert-danger');
        $('.alert').removeAttr('hidden');
      }
    },
    error: function(request, status, error){
        $('.alert').prepend("<strong>Error</strong> "+error);
        $('.alert').toggleClass('alert-danger');
        $('.alert').removeAttr('hidden');
    }
  });
});
