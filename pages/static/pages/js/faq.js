(function ($) {

$(function () {
  if (window.location.hash) {
    var el = $(window.location.hash);
    el.addClass('active');
    $('body').scrollTop($('body').scrollTop() - $(el).prev().height());
  }
});

$('.accordion .content').on('toggled', function () {
  $('.accordion .content').not(this).removeClass('active');   // Close others.
  var isActive = $(this).hasClass('active');
  window.location.hash = isActive ? '#' + this.id : '';
  if (isActive)
    $('body').scrollTop($('body').scrollTop() - $(this).prev().height() * 2);
});

})(jQuery);
