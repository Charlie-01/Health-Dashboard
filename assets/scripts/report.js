function gatherReportData() {
    var dataobj = {};

    // These values would be stored in a session cookie upon user authentication
    // dataobj['patient_id'] = Math.floor(100*Math.random());
    // dataobj['doctor_id'] = Math.floor(100*Math.random());
    dataobj['patient_id'] = 420;
    dataobj['doctor_id'] = 69;
    
    var age = $("#age").val();
    dataobj['age'] = parseInt(age);

    var sex = $("#sex").val();
    dataobj["sex"] = parseInt(sex);

    var weight = $("#weight").val();
    dataobj["weight"] = parseInt(weight);

    var height = $("#height").val();
    dataobj["height"] = parseInt(height);

    var race = $("#race").val();
    dataobj["race"] = parseInt(race);

    //stores the stuff checked in general into data obj    

    var categories = ["general","dermatology","psychiatric",
    "cardiac","gastric","skeletal","urinary","respiratory"]

    var j;
    for(j = 0;j < categories.length;j++){
        var name = "#" + categories[j]+":checked";
        var cboxes = $(name);
        var temp = [];
        var i;
        for(i = 0; i < cboxes.length; i++){
            temp.push(cboxes[i].value)
        }
        if(temp.length != 0){
            dataobj[categories[j]] = temp;
        }
    }

    var myJSON = JSON.stringify(dataobj);
    console.log(myJSON);

    $("#frm")[0].reset();
    var xhttp = new XMLHttpRequest();
    xhttp.open("POST", "https://scheduleyourappointment.online/api/database_interaction/report", true);
    xhttp.setRequestHeader("Content-type", "application/json");
    xhttp.send(myJSON);

}
