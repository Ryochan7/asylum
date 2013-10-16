var openDropdownTimer = null;

function checkOpenDropdown(item) {

    if (item.hasClass("open"))
    {
      item.removeClass("open");
      openDropdownTimer = null;
    }
};

$(document).ready(function(){
  
    $('.p2col .span6:even').addClass('no-margin-left');

    //prettyPhoto
    $('a[data-rel]').each(function() {
        $(this).attr('rel', $(this).data('rel'));
    });
    $("a[rel^='prettyPhoto']").prettyPhoto();


    $('.da-thumbs > li, .da-thumbs > article').hoverdir();

    $("#top-nav-menu li.dropdown").hover(function () {
      if (openDropdownTimer)
      {
	clearTimeout(openDropdownTimer);
	openDropdownTimer = null;
      }
      
      $(this).addClass("open");
    }, function () {
      var listItem = $(this);

      openDropdownTimer = setTimeout(function(){
	checkOpenDropdown(listItem);
      }, 1000);
    });
    
    $(".our-blog article").hover(function () {
    	$(this).find("img").stop(true, true).animate({ opacity: 0.7 }, 300);
    }, function() {
    	$(this).find("img").stop(true, true).animate({ opacity: 1 }, 300);
    });
    
    
    //Flickr Widget Footer
    /*$('#footer .flickr').jflickrfeed({
		limit: 6,
		qstrings: {
			id: '36621592@N06'
		},
		itemTemplate: '<li>'+
						'<a rel="prettyPhoto[flickr]" href="{{image}}" title="{{title}}">' +
							'<img src="{{image_s}}" alt="{{title}}" />' +
						'</a>' +
					  '</li>'
	}, function(data) {
		$("a[rel^='prettyPhoto']").prettyPhoto();

        $("#footer .flickr li").hover(function () {						 
    	   $(this).find("img").stop(true, true).animate({ opacity: 0.5 }, 800);
        }, function() {
    	   $(this).find("img").stop(true, true).animate({ opacity: 1.0 }, 800);
        });
	});*/


	//Flickr Widget Sidebar
    /*$('#sidebar .sidebar-flickr').jflickrfeed({
		limit: 8,
		qstrings: {
			id: '36621592@N06'
		},
		itemTemplate: '<li>'+
						'<a rel="prettyPhoto[flickr]" href="{{image}}" title="{{title}}">' +
							'<img src="{{image_s}}" alt="{{title}}" />' +
						'</a>' +
					  '</li>'
	}, function(data) {
		$("a[rel^='prettyPhoto']").prettyPhoto();

        $("#footer .flickr li").hover(function () {						 
    	   $(this).find("img").stop(true, true).animate({ opacity: 0.5 }, 800);
        }, function() {
    	   $(this).find("img").stop(true, true).animate({ opacity: 1.0 }, 800);
        });
	});*/


	//Portfolio
	var $portfolioClone = $(".filtrable").clone();
	$("#filtrable a").live('click', function(e){
		
		$("#filtrable li").removeClass("current");	
		
		var $filterClass = $(this).parent().attr("class");
        var $filteredPortfolio = $portfolioClone.find("article");

		if ( $filterClass == "all" ) {
			$filteredPortfolio = $portfolioClone.find("article");
		} else {
			$filteredPortfolio = $portfolioClone.find("article[data-type~=" + $filterClass + "]");
		}
	
		$(".filtrable").quicksand( $filteredPortfolio, { 
			duration: 800, 
			easing: 'easeOutQuint' 
		}, function(){
			
            $('.da-thumbs > li, .da-thumbs > article, .da-thumbs > div').hoverdir();
            
            $("a[rel^='prettyPhoto']").prettyPhoto();

		});

		$(this).parent().addClass("current");
        
		e.preventDefault();
	});

    // To Top Button
    $(function(){
        $().UItoTop({ easingType: 'easeOutQuart' });
    });

    // portfolio ie fix
    /*if ($.browser.msie && $.browser.version > "10") {
        $(function(){
            $('.hover-span').mouseenter(function(){
                alert('enter')
            });
            $('.hover-span').mouseleave(function(){
                alert('leave')
            });
        });
    }
    else {
    }*/



});


$(window).load(function() {

	$("#mainslider").flexslider({
		animation: "slide",
		useCSS: false,
		controlNav: false,   
		animationLoop: true,
		smoothHeight: true
	});

    $(function () {
        $(".lightbox-image").append("<span></span>");
        $(".lightbox-image").hover(function () {
            $(this).find("img").stop().animate({opacity:0.5}, "normal")
        }, function () {
            $(this).find("img").stop().animate({opacity:1}, "normal")
        })
    });
});
