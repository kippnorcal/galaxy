$(function() {
  var page = window.location.href;
  $.ajax({
    data: {'page': page},
    type: 'POST',
    url: '/pageview/',
  });
});
