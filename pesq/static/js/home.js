function sticky_relocate2() {
  var window_top = $(window).scrollTop();
  var window_bottom = $(window).scrollTop() + $(window).height();
  var div_top = $("#content2-anchor").offset().top;
  var div_bottom = $("footer").offset().top
  var footerH =  $("footer").height() ;
  var subH = $("#subscribe2").height() ;
  var dif = div_bottom -footerH
  if (window_top > div_top-150 && window_bottom < dif) {
    $("#sticky2").addClass("stick");
    $("#sticky2-phantom").show();
    $("#sticky2").show();
  } else {
    $("#sticky2").removeClass("stick");
    $("#sticky2-phantom").hide();
    $("#sticky2").hide();
  }
}

$(function() {
    $(window).scroll(sticky_relocate2);
    sticky_relocate2();
  });


$(".cronograma-plus").on('click',  function() {
  if($(this).siblings(".cronograma-item-content").is(':visible')){
    $(this).siblings(".cronograma-item-content").hide();
  }else{
    $(this).siblings(".cronograma-item-content").show();
  }

});
