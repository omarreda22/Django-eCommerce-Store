//NOTE: This is not my original code. 
//I found this snippet on a website titled Dev Ingredients. http://devingredients.com/2011/11/building-an-extensible-jquery-countdown-plugin-from-scratch
//Dev Ingredients is managed by Catalin Berta. 
//I'm placing the code here to explore it further, for learning purposes.

(function($) {
  $.fn.countdown = function(options, callback) {
    //custom 'this' selector
    thisEl = $(this); 
  
    // array of custom settings
    var settings = { 
      'date': null,
      'format': null
    };

    // append the settings array to options
    if(options) {
      $.extend(settings, options);
    }
   
    //create the countdown processing function
    function countdown_proc() {
    var eventDate = Date.parse(settings.date) / 1000;
    var currentDate = Math.floor($.now() / 1000);
    
    if(eventDate <= currentDate) {
    callback.call(this);
    clearInterval(interval);
    }
      
    var seconds = eventDate - currentDate;
    
    var days = Math.floor(seconds / (60 * 60 * 24)); 
    //calculate the number of days
    
    seconds -= days * 60 * 60 * 24; 
    //update the seconds variable with number of days removed
    
    var hours = Math.floor(seconds / (60 * 60));
    seconds -= hours * 60 * 60; 
    //update the seconds variable with number of hours removed
    
    var minutes = Math.floor(seconds / 60);
    seconds -= minutes * 60; 
    //update the seconds variable with number of minutes removed
    
    //conditional statements
    if (days == 1) { thisEl.find(".timeRefDays").text("day"); } else { thisEl.find(".timeRefDays").text("days"); }
		    if (hours == 1) { thisEl.find(".timeRefHours").text("hour"); } else { thisEl.find(".timeRefHours").text("hours"); }
		    if (minutes == 1) { thisEl.find(".timeRefMinutes").text("mins"); } else { thisEl.find(".timeRefMinutes").text("mins"); }
		    if (seconds == 1) { thisEl.find(".timeRefSeconds").text("secs"); } else { thisEl.find(".timeRefSeconds").text("secs"); }
    
    //logic for the two_digits ON setting
    if(settings.format == "on") {
        days = (String(days).length >= 2) ? days : "0" + days;
        hours = (String(hours).length >= 2) ? hours : "0" + hours;
        minutes = (String(minutes).length >= 2) ? minutes : "0" + minutes;
        seconds = (String(seconds).length >= 2) ? seconds : "0" + seconds;
    }
    
    //update the countdown's html values.
    thisEl.find(".days").text(days);
    thisEl.find(".hours").text(hours);
    thisEl.find(".minutes").text(minutes);
    thisEl.find(".seconds").text(seconds);
  }

	//run the function
	countdown_proc();

	//loop the function
	interval = setInterval(countdown_proc, 1000);
  };

}) (jQuery);


//Provide the plugin settings
// $("#countdown-1,#countdown-2").countdown({
// 	//The countdown end date
// 	date: "25 jun 2017 01:00:00",
// 
// 	// on (03:07:52) | off (3:7:52) - two_digits set to ON maintains layout consistency
// 	format: "on"
// 	}, 
// 
// });