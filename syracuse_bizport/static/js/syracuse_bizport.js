// Freelancer Theme JavaScript

(function($) {
    "use strict"; // Start of use strict

    // jQuery for minimizing logo on scroll down page

    $(window).scroll(function(){
      var scroll = $(window).scrollTop();
      // Minimize if the user scrolls more than 50px
      if(scroll >= 50){
        // This just adds a class, the rest is CSS
        $('#main-logo').addClass('minimized');
      } else {
        $('#main-logo').removeClass('minimized');
      }
    });

    // jQuery for page scrolling feature - requires jQuery Easing plugin
    $('.page-scroll a').bind('click', function(event) {
        var $anchor = $(this);
        $('html, body').stop().animate({
            scrollTop: ($($anchor.attr('href')).offset().top - 50)
        }, 1250, 'easeInOutExpo');
        event.preventDefault();
    });

    // Closes the Responsive Menu on Menu Item Click
    $('.navbar-collapse ul li a').click(function(){
            $('.navbar-toggle:visible').click();
    });

    // Affixed checklist
    function affixChecklist(){
      $('.sidebar-checklist').affix({
        offset: {
          top: 185,
          bottom: 350
        }
      });
    }

    // Initial load: If the user is on a large screen, show the affixed checklist
    if($(window).width() > 768){
      affixChecklist();
    }

    // On resize, affix the checklist if the window is large
    // otherwise unbind bootstrap affix
    $(window).resize(function(){
      var viewPortWidth = $(window).width();
      if(viewPortWidth > 768){
        affixChecklist();
      } else {
        $(window).off(".affix");
        $(".sidebar-checklist")
          .removeClass("affix affix-top affix-bottom")
          .removeData("bs.affix");
      }
    })

    // Floating label headings for the contact form
    $(function() {
        $("body").on("input propertychange", ".floating-label-form-group", function(e) {
            $(this).toggleClass("floating-label-form-group-with-value", !!$(e.target).val());
        }).on("focus", ".floating-label-form-group", function() {
            $(this).addClass("floating-label-form-group-with-focus");
        }).on("blur", ".floating-label-form-group", function() {
            $(this).removeClass("floating-label-form-group-with-focus");
        });
    });

})(jQuery); // End of use strict
