/*
variables
*/
var fakeDataX = [4, 2, 5, 20, 20, 1, 5, 3]


/*
scrape hashtag that the user enters
*/
function Get_User_Hashtag() {
	var x = document.getElementById("user_hashtag").value;
	document.getElementById("report_display").innerHTML = x;
}

function run_NB() {
	model = Setup_model();
    prediction = model.predict(fakeDataX);
    console.log(prediction);
    prediction = model.predict([1,1,1,1,1,1,1,1])
    console.log(prediction);
}