function prepareDocument () {
	$("form#search").submit(function(){
		text=$("id_q").val();
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
}
$(document).ready(prepareDocument); //jQuery’s ready() function is that your events can fire as soon as the DOM is ready