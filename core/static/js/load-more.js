(function ($) {
 "use strict";

//load more jquery
	var list1 = $(".load-list-one li");
	var list2 = $(".load-list-two li");
	var list3 = $(".load-list-three li");
	var list4 = $(".load-list-four li");
	var list5 = $(".load-list-blog li");
	
	var numToShow1 = 1;
	var numToShow2 = 2;
	var numToShow3 = 2;
	var numToShow4 = 2;
	var numToShow5 = 1;
	
	var button1 = $("#load-more-one");
	var button2 = $("#load-more-two");
	var button3 = $("#load-more-three");
	var button4 = $("#load-more-four");
	var button5 = $("#load-more-blog");
	
	var numInList1 = list1.length;
	var numInList2 = list2.length;
	var numInList3 = list3.length;
	var numInList4 = list4.length;
	var numInList5 = list5.length;
	
	list1.hide();
	list2.hide();
	list3.hide();
	list4.hide();
	list5.hide();
	
	if (numInList1 > numToShow1) {
		button1.show();
	}
	if (numInList2 > numToShow2) {
		button2.show();
	}
	if (numInList3 > numToShow3) {
		button3.show();
	}
	if (numInList4 > numToShow4) {
		button4.show();
	}
	if (numInList5 > numToShow5) {
		button5.show();
	}
	list1.slice(0, numToShow1).show();
	list2.slice(0, numToShow2).show();
	list3.slice(0, numToShow3).show();
	list4.slice(0, numToShow4).show();
	list5.slice(0, numToShow5).show();

	button1.click(function(){
		var showing1 = list1.filter(':visible').length;
		list1.slice(showing1 - 1, showing1 + numToShow1).fadeIn();
		var nowShowing1 = list1.filter(':visible').length;
		if (nowShowing1 >= numInList1) {
		button1.hide();
		}
	});
	button2.click(function(){
		var showing2 = list2.filter(':visible').length;
		list2.slice(showing2 - 1, showing2 + numToShow2).fadeIn();
		var nowShowing2 = list2.filter(':visible').length;
		if (nowShowing2 >= numInList2) {
		button2.hide();
		}
	});
	button3.click(function(){
		var showing3 = list3.filter(':visible').length;
		list3.slice(showing3 - 1, showing3 + numToShow3).fadeIn();
		var nowShowing3 = list3.filter(':visible').length;
		if (nowShowing3 >= numInList3) {
		button3.hide();
		}
	});
	button4.click(function(){
		var showing4 = list4.filter(':visible').length;
		list4.slice(showing4 - 1, showing4 + numToShow4).fadeIn();
		var nowShowing4 = list4.filter(':visible').length;
		if (nowShowing4 >= numInList4) {
		button4.hide();
		}
	});
	button5.click(function(){
		var showing5 = list5.filter(':visible').length;
		list5.slice(showing5 - 1, showing5 + numToShow5).fadeIn();
		var nowShowing5 = list5.filter(':visible').length;
		if (nowShowing5 >= numInList5) {
		button5.hide();
		}
	});
	
	
})(jQuery); 