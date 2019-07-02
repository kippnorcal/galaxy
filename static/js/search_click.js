$('.search_link').click(function(){
  var search_id = $('#search-id').data('search');
  var destination = $(this).attr('href');
  console.log(destination);
  $.ajax({
    data: {'destination': destination},
    type: 'POST',
    url: 'click_through/'+search_id,
  });
});

