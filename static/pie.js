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
//}

function autofill(){
    var x = document.getElementById('main_type').value;
    if(x=='Annual Maintenance-Spares')
    {
        document.getElementById("period").value= 1;
    }
}

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

function changeValue(){
    var y=event.target.id
    var x=event.target.value
//    document.getElementById('userupdate'+parseInt(y)).style.display = 'block';
    var userdata = [{'item' : y},{'price' : x}];
    $.ajax({
    type: "POST",
    url: "/ProcessPrice",
    data: JSON.stringify(userdata),
    contentType: "application/json",
    dataType: 'json'
    });
//    window.location.reload();
}

function UserUpdate(){
var y=event.target.id
document.getElementById(y).style.display = 'none';
}

function checkPeriod(){
var x=event.target.value
if (x > 10 ) {
    Swal.fire('Good job!','Periodity should be less than 10 years!','success')("periodity should be less than 10 years");
    }
}
function popupWindow(url, windowName, win, w, h) {
    const y = win.top.outerHeight / 2 + win.top.screenY - ( h / 2);
    const x = win.top.outerWidth / 2 + win.top.screenX - ( w / 2);
    return win.open(url, windowName, `toolbar=no, location=no, directories=no, status=no, menubar=no, scrollbars=no, resizable=no, copyhistory=no, width=${w}, height=${h}, top=${y}, left=${x}`);
}


function submitForm(elem) {
    if (elem.value) {
    elem.form.submit();
    }
    var y=event.target.id
    var x=event.target.value
//    document.getElementById('y').value='x' ;
//    document.getElementById('userupdate'+parseInt(y)).style.display = 'block';
    var userdata = [{'item' : y},{'price' : x}];
    $.ajax({
    type: "POST",
    url: "/ProcessPrice",
    data: JSON.stringify(userdata),
    contentType: "application/json",
    dataType: 'json'
    });
}
//ОГРАНИЧЕНИЕ ВСТАВКИ ТЕКСТА!!!
//https://medium.com/@sampathsl/how-to-restrict-an-input-field-for-numeric-using-javascript-34142773a102