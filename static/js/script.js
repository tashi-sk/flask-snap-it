// to show and hide edit/delete comments 
$(document).ready(function () {
  $(".drop-down").click(function() {
    $(this).parent().prev().toggle()
    $(this).next().css('display', 'block');
    $(this).css('display', 'none');
  });
  $('.cross').click(function(){
    $(this).parent().prev().toggle()
    $(this).css('display', 'none');
    $(this).prev().css('display','block')
  })
});