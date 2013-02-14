$('#bm_show-build-info').hover(function() {
    $('#bm_show-build-info').css('opacity', '1');
    $('#bm_build-info').css('display', 'inline');
}, function() {

});

$('#bm_footer-right').hover(function() {}, function()
{
    $('#bm_build-info').css('display', 'none');
    $('#bm_show-build-info').css('opacity', '.1');
});