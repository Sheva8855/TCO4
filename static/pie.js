//    <script type ="text/javascript" src="https://cdn.anychart.com/releases/8.0.1/js/anychart-core.min.js"></script>
//    <script type ="text/javascript" src="https://cdn.anychart.com/releases/8.0.1/js/anychart-pie.min.js"></script>


//anychart.onDocumentReady(function() {
//
//for (let i = 0; i < component_names.length; i++) {
//  text += cars[i] + "<br>";
//}
//  var data = [
//      {x: "White", value: 223553265},
//      {x: "Black", value: 38929319},
//      {x: "Red", value: 2932248},
//      {x: "Yellow", value: 14674252},
//      {x: "Green", value: 540013},
//      {x: "Brown", value: 19107368},
//      {x: "Purple", value: 9009073}
//  ];
//  for (let i = 0; i < component_names.length; i++) {
//
//  var data1 = [
//      {x: component_names[i], value: component_prices[i]},
//  ];
//}
//  // create the chart
//  var chart = anychart.pie();
//
//  // set the chart title
//  chart.title("CAPEX for item");
//
//  // add the data
//  chart.data(data1);
//
//  // display the chart in the container
//  chart.container('container2');
//  chart.draw();
//});


}

function autofill(){
    var x = document.getElementById('main_type').value;
    if(x=='Annual Maintenance-Spares')
    {
        document.getElementById("period").value= 1;
    }
}

//$( document ).ready(function() {
//    $("#btn6").click(
//		function(){
////		    document.getElementById('result_form').innerHTML ='<br>Some new content!';
//        	$('#result_form').html('Имя: ');
//
////			sendAjaxForm('result_form', 'ajax_form', 'action_ajax_form.php');
//			return true;
//		}
//	);
//});
var component_names = localStorage.getItem("someVarKey");
if (component_names=null) {
  component_names=[]
}
var component_prices=[];
var component_comments=[];

function addsmth(){
    var x=document.getElementById("component_name").value;
    var y=document.getElementById("component_price1").value;
    var z=document.getElementById("component_comment").value;
    component_names.push(x);
    localStorage.setItem("someVarKey", component_names);
    component_prices.push(y);
    component_comments.push(z);
    document.getElementById('result_form').innerHTML = component_names+component_prices+component_comments;
    document.getElementById("component_name").value ='';
    document.getElementById("component_price1").value ='';
    document.getElementById("component_comment").value ='';
}




