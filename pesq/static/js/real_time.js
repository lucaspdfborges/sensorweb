
$(document).load(function(){

  $(".box-title").click(function(){
     var content =  $(this).closest('.box').find('.box-content');
     var contentHeight = content.css('height');
     var arrow = $(this).closest('.box').find('.box-arrow');

    if(contentHeight > '0px'){
       content.css('height','0');
       arrow.addClass('fa-chevron-right').removeClass('fa-chevron-down');
    } else{
       content.css('height','50');
       arrow.addClass('fa-chevron-down').removeClass('fa-chevron-right');
    }

  });

});
