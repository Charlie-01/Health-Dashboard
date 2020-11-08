window.onload = getRiskProfile(420)

function graph(JSON_Obj) {

    function compare(a, b) {
        // Use toUpperCase() to ignore character casing
        const dateA = Number(a.x);
        const dateB = Number(b.x);
      
        let comparison = 0;
        if (dateA > dateB) {
          comparison = 1;
        } else if (dateA < dateB) {
          comparison = -1;
        }
        return comparison;
      }

    var data = [];
    
    //array of risk evals
    console.log(JSON_Obj.risk_evaluations);

    var i;
    var risk_array = JSON_Obj.risk_evaluations
    for(i = 0; i < 10;i++){
        var obj = {};
        var risk_index = risk_array[i].risks[0].index;
        var datestring = risk_array[i].report_time.split(" ")[0];
        var datearray = datestring.split("-");
        var month = datearray[1]-(i+1);
        var year = datearray[0]-(i+1);
        var day = datearray[2]-(i+1);
        if(day <= 0){day = 28;}
        if(month <= 0){month = 12}
        /*
        var risk_index = risk_array[i].risks[0].index;
        var month = Math.ceil(Math.random() * 12);
        var day = Math.ceil(Math.random() * 30);
        var max = 2020;
        var min = 2000;
        var year = Math.ceil(Math.random() * (max - min) + min);
        */
        year 
        obj.x = new Date(year, month, day);
        obj.y = risk_index;
        data.push(obj);
    }
    for(i = 10; i < risk_array.length;i++){
        var obj = {};
        var risk_index = risk_array[i].risks[0].index;
        var datestring = risk_array[i].report_time.split(" ")[0];
        var datearray = datestring.split("-");
        var month = datearray[1];
        var year = datearray[0];
        var day = datearray[2];
        obj.x = new Date(year, month, day);
        obj.y = risk_index;
        data.push(obj);
    }

    console.log(data);
    data.sort(compare);
    console.log(data);

  var chart = new CanvasJS.Chart("chartContainer",
  {

    title:{
    text: "Health Risk"
    },
     data: [
    {
      type: "line",

      dataPoints: data
    }
    ]
  });

  chart.render();
}

function parseResponse(text) {
  return JSON.parse(text);
}

function getRiskProfile(id) {
  xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function () {
    if (this.readyState == 4 && this.status == 200) {
        tmp = parseResponse(this.responseText);
        return graph(tmp);
    }
  };
  xhttp.open("GET", "https://scheduleyourappointment.online/api/database_interaction/internal?patient_id=" + id, true);
  xhttp.send();
}