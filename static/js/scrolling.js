$(window).scroll(function() {
    var scroll = $(window).scrollTop();
    document.getElementById("myFirst").style.marginTop = (-100 - 0.5 * scroll) + "px";

    if(scroll >= 200) {
        $("#myNav").addClass("bg-dark");
    }
    else {
        $("#myNav").removeClass("bg-dark");
    }
});