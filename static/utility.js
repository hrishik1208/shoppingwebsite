function submitData(targetURL) {
	//Marshelling into JSON
	var dataToBeSent = "{";
	if(typeof(document.forms[0]) == 'undefined' || document.forms[0] == null){
		alert("HTML form element is not defined.");
		return;
	}
	var x = document.forms[0].elements;
	for (var i = 0; i < x.length; i++) {			
		if((x[i].getAttribute("type") != null) && 
			(x[i].getAttribute("type").toLowerCase() == 'submit' || x[i].getAttribute("type").toLowerCase() == 'button')) continue;
		
		if(i > 0) dataToBeSent += ",";
		dataToBeSent += "\""+ x[i].getAttribute("name") +"\":\""+ x[i].value +"\"";
	}
	dataToBeSent += "}";
	dataToBeSent = JSON.stringify(dataToBeSent);
	
	//Sending HTTP request to server
	sendRequest(targetURL, dataToBeSent);
	
	return false;
}

function sendRequest(targetURL, jsonData){
	var xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function() {
		if (this.readyState == 4 && this.status == 200) {
			showOutput(this.responseText);
		} else if (this.readyState == 4){
			alert("Error occurred with status code: "+this.status);
		}
	};
	xhttp.open("POST", targetURL, true);
	xhttp.setRequestHeader("Content-type", "application/json");
	xhttp.send(jsonData);
}

function showOutput(output){		
	var division = document.getElementById("output_div");
	if(division === null || division == 'undefined'){			
		division = document.createElement("div");	
		division.setAttribute("id", "output_div");	
		division.setAttribute("style", "text-align:center");
		division.style.color = "blue";	
		var element = document.getElementsByTagName("body");
		element[0].appendChild(division);
	}		
	division.innerHTML = output
}
