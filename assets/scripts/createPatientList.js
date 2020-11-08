window.onload = getPatients();

function parseResponse(text) {
    return JSON.parse(text);
}

function getPatients() {
    xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
      if (this.readyState == 4 && this.status == 200) {
          tmp = parseResponse(this.responseText);
          return loadPatients(tmp);
      }
    };
    xhttp.open("GET", "https://scheduleyourappointment.online/api/database_interaction/patient?patient_id=all", true);
    xhttp.send();
  }

  function loadPatients(JSON_obj) {
      console.log(JSON_obj);

      var patient__array = JSON_obj;

      var appointmentContainer = document.getElementsByClassName("patient__display")[0];
      var appointments = appointmentContainer.getElementsByTagName("div")
      
      var i;
      for(i = 0;i < 3;i++){
        var id = patient__array[i].id;
        var index = patient__array[i].doc.patient_risk_level;
        index = index.toFixed(2);

        var ps = appointments[i].getElementsByTagName("p");
        for (let j = 0; j < 2; j++) {
            if (j == 0) {
                ps[j].innerHTML = "Patient: " + id;
            } else {
                ps[j].innerHTML = "Risk: " + index + "%";
            }
        }
        
      }
  }