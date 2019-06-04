$('.fav-btn').click(function(event){
  event.preventDefault();
  form = $('#favoriteform')
  $.ajax({
    data: form.serialize(),
    type: form.attr('method'),
    url: form.attr('action'),
    success: function(response){
      if(response['success']){
        $('.fav-btn').toggleClass('far').toggleClass('fas');
        $('.fav-badge').text(response['favorited_by']);
      }
    },
    error: function(request, status, error){
      $('.alert').prepend("<strong>Error</strong> "+error);
      $('.alert').toggleClass('alert-danger');
      $('.alert').removeAttr('hidden');
    }
  });
});

