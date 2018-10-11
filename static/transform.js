function transform(json){
    json.PET_WEIGHT = json.PET_WEIGHT + 'kg';
    json.PET_ADMS = (json.PET_ADMS == 0)? '내원' : '외래';
    switch(json.PET_SEX){
        case '0' :
            json.PET_SEX = 'female';
            break;
        case '1' :
            json.PET_SEX = 'male';
            break;
        case '2':
            json.PET_SEX = 'castrated female';
            break;
        case '3' :
            json.PET_SEX = 'castrated male';
            break;
    }
    json.PET_CONTACT = json.PET_CONTACT.replace(/-/gi, ' - ');
    return json;
}

function appendDisease(name, disease_id){
    var idArr1 = [];
    var list1 = $(".searched-result-list-item1");
    $.each(list1, function () {

        idArr1.push($(this).html());
     });
     if(!idArr1.includes(name.split("(")[0])){
        $("#searched1").append("<div class='searched-result-list-item1' data-select='0' data-item='"+disease_id+"'>"+name.split("(")[0]+"</span>");
     }

}
function searchMedicine(){
    var idArr1 = [];
    var list1 = $(".searched-result-list-item1");
    $.each(list1, function () {
        if($(this).attr("data-select") == 1)
            idArr1.push($(this).attr('data-item'));
     });

//                var idArr2 = [];
//                var list2 = $(".searched2");
//                $.each(list2, function () {
//                    if($(this).attr("data-select") == 1)
//                        idArr2.push($(this).html());
//                 });
    $.ajax({
        type: "POST",
        url: "/load_medicine",
        dataType: 'json',
        data: { word1: idArr1 }, // stringify
        success: function(data){
            $("#medicine-category").empty();
            for(var i=0;i<data.length;i++){
                $("#medicine-category").append("<div class='medicine-categorys' data-item='"+data[i].MEDI_ID+"'>" + data[i].MEDI_NAME + "</div>");
            }
        }
    });
}

function searchDisease(){
    var idArr1 = [];
    var list1 = $(".searched-result-list-item1");
    $.each(list1, function () {
        //if($(this).attr("data-select") == 1)
            idArr1.push($(this).html());
     });

    var idArr2 = [];
    var list2 = $(".searched-result-list-item2");
    $.each(list2, function () {
        //if($(this).attr("data-select") == 1)
            idArr2.push($(this).html());
     });
    $.ajax({
        type: "POST",
        url: "/load_disease",
        dataType: 'json',
        data: { word1: idArr1, word2: idArr2 }, // stringify
        success: function(data){
            for(var i=0;i<data.length;i++){
                //중복검사
                appendDisease(data[i].DISEASE_NAME, data[i].DESEASE_ID);
            }
        }
    });
}