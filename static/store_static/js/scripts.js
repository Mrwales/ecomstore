function prepareDocument(){
	$("form#search").submit(function(){
	text=$("#id_q").val();
		if(text=="" || text=="Search"){
			alert("Enter a search term.");
			return false;		
		}
	});
	
}

$(document).ready(prepareDocument);//fire event as soon as the DOM is ready

