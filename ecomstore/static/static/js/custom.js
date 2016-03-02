function prepareDocument(){
	$("form#search").submit(function(){
	text=$("#id_q").val();
		if(text=="" || text=="Search"){
			alert("Enter a search term.");
			return false;		
		}
	});
	$("#submit_review").click(addProductReview);
	//$("#review_form").addClass('hidden');
	$("#add_review").click(slideToggleReviewForm);
	$("#add_review").addClass('visible');
	$("#cancel_review").click(slideToggleReviewForm);
	$("#add_tag").click(addTag);
	$("#id_tag").keypress(function(event){
		if (event.keyCode == 13 && jQuery("#id_tag").val().length > 2){//Key code 13 corresponds to the Enter key
			addTag();
			event.preventDefault();
		}
	});
	function statusBox(){
		$('<div id="loading">Loading...</div>').prependTo("#status")
		.ajaxStart(function(){jQuery(this).show();})
		.ajaxStop(function(){jQuery(this).hide();})
}
	
}
function slideToggleReviewForm(){
	$("#review_form").slideToggle();/*jQuery’s slideToggle() function slowly brings hidden elements into view, and visible elements out of sight, using a sliding vertical-accordion visual effect */
	$("#add_review").slideToggle();
}
function addTag(){
	tag={
		tag:$("#id_tag").val(),
		slug:$("#id_slug").val(),
		csrfmiddlewaretoken:$("input[name=csrfmiddlewaretoken]").val(),
		}
	$.post("/tag/product/add/",tag,
			function(response){
			if(response.success=="True"){
				$("#tags").empty();
				$("#tags").append(response.html);
				$("#id_tag").val("");
			}			
			},
			"json");
}
function addProductReview () {
	// build an object of review data to submit
	var review={
		title:$("#id_title").val(),
		content:$("#id_content").val(),
		rating:$("#id_rating").val(),
		slug:$("#id_slug").val(),
		csrfmiddlewaretoken:$("input[name=csrfmiddlewaretoken]").val(),
	};
	//make request, process response
	$.post("/review/product/add/",review,
				function(response){
					$("#review_errors").empty();
					//evaluate the suucces parameter
					if(response.success == "True"){
						// disable the submit button to prevent duplicates
						$("#submit_review").attr('disabled','disabled');
						// if this is first review, get rid of "no reviews" text
						$("#no_reviews").empty();
						$("#reviews").prepend(response.html).slideDown();
						new_review=$("#reviews").children(":first");
						//hide the review form
						$("#review_form").slideToggle();
					}else{
						$("#review_errors").append(response.html);
					}
				},"json"
	);
}
$(document).ready(prepareDocument);//fire event as soon as the DOM is ready

