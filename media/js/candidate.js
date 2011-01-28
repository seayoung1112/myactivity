$(function(){
  $(".unhandle > .candidate").click(function(){
    $(this).toggleClass('select');
    var cbox = $(this).find("input:checkbox");
    cbox.attr("checked", !cbox.attr("checked"));
  });
  $('.unhandle').removeClass("unhandle");
});

