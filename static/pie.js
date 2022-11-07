//    <script type ="text/javascript" src="https://cdn.anychart.com/releases/8.0.1/js/anychart-core.min.js"></script>
//    <script type ="text/javascript" src="https://cdn.anychart.com/releases/8.0.1/js/anychart-pie.min.js"></script>
document.getElementById('container4').innerHTML += '<br>Some new content!';

anychart.onDocumentReady(function() {

  var data = [
      {x: "White", value: 223553265},
      {x: "Black", value: 38929319},
      {x: "Red", value: 2932248},
      {x: "Yellow", value: 14674252},
      {x: "Green", value: 540013},
      {x: "Brown", value: 19107368},
      {x: "Purple", value: 9009073}
  ];

  // create the chart
  var chart = anychart.pie();

  // set the chart title
  chart.title("CAPEX for item");

  // add the data
  chart.data(data);

  // display the chart in the container
  chart.container('container2');
  chart.draw();
});

    var plane;
    var popular;

    var Array1=[];
    var Array2=[];
    var components=[];
//function addcomponents(){
//  //Assign values
//  plane=document.getElementById("plane");
//  popular=document.getElementById("popular");
//  Array1.push(plane);
//  Array2.push(popular);
//  components=[Array1,Array2];
//  console.log(Array1);
//  console.log(Array2);
//  console.log(components);
//
//  //output the results
////  document.getElementById("container3").innerHTML = 7+9;
////  document.getElementById('container3').innerHTML =plane;
//  document.getElementById('container3').innerHTML = 7+'<br>Some new content!';
//  return true;
}