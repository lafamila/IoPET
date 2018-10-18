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
function appendMedicine(name, medicine_id){
    var idArr1 = [];
    var list1 = $(".medicine-categorys");
    $.each(list1, function () {

        idArr1.push($(this).html());
    });
    if(!idArr1.includes(name)){
        var $div = $('<div/>');
        $div.addClass('medicine-categorys')
            .html(name)
            .data('id', medicine_id);


        $.ajax({
                                   url : '/load_medicine_by_id',
                                    success : function(data){

                                            $div.data('intro', data.MEDI_INTRO)
                                                   .data('side', data.MEDI_SIDE)
                                                   .data('warn', data.MEDI_WARN)
                                                   .data('vol', data.MEDI_VOL)
                                                   .data('period', data.MEDI_PERIOD)
                                                   .data('method', data.MEDI_METHOD)
                                                   .data('doses', data.MEDI_DOSES)
                                                   .data('price', data.MEDI_PRICE);


                                    },
                                    type : 'post',
                                    dataType: 'json',
                                    data : {iid : medicine_id}
                                });

        $("#medicine-category").append($div);
    }
}

function appendDisease(name, disease_id, recommend){
    var idArr1 = [];
    var list1 = $(".searched-result-list-item1");
    $.each(list1, function () {

        idArr1.push($(this).html());
     });
     if(!idArr1.includes(name.split("(")[0])){
        $("#searched1").append("<div class='searched-result-list-item1' data-select='0' data-item='"+disease_id+"' data-recommend='"+recommend+"'>"+name.split("(")[0]+"</span>");
     }

}
function searchMedicine(){
    var idArr1 = [];
    var list1 = $(".searched-result-list-item1");
    $.each(list1, function () {
        if($(this).attr("data-select") == 1)
            idArr1.push($(this).attr('data-item'));
     });
     if(list1.length>0){
        $.ajax({
            type: "POST",
            url: "/load_medicine",
            dataType: 'json',
            data: { word1: idArr1 }, // stringify
            success: function(data){
                $("#medicine-category").empty();
                $("#medicine").empty();
                for(var i=0;i<data.length;i++){
                    var $div = $('<div/>');
                    $div.addClass('medicine-categorys')
                        .html(data[i].MEDI_NAME)
                        .data('id', data[i].MEDI_ID)
                        .data('intro', data[i].MEDI_INTRO)
                        .data('side', data[i].MEDI_SIDE)
                        .data('warn', data[i].MEDI_WARN)
                        .data('vol', data[i].MEDI_VOL)
                        .data('period', data[i].MEDI_PERIOD)
                        .data('method', data[i].MEDI_METHOD)
                        .data('doses', data[i].MEDI_DOSES)
                        .data('price', data[i].MEDI_PRICE);

                    $("#medicine-category").append($div);
                }
            }
        });
     }

//                var idArr2 = [];
//                var list2 = $(".searched2");
//                $.each(list2, function () {
//                    if($(this).attr("data-select") == 1)
//                        idArr2.push($(this).html());
//                 });

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
                appendDisease(data[i].DISEASE_NAME, data[i].DISEASE_ID, data[i].DISEASE_RECOMMEND);
            }
        }
    });
}


function CommaFormatted(amount) {
	var delimiter = ","; // replace comma if desired
	var i = parseInt(amount);
	if(isNaN(i)) { return ''; }
	var minus = '';
	if(i < 0) { minus = '-'; }
	i = Math.abs(i);
	var n = new String(i);
	var a = [];
	while(n.length > 3) {
		var nn = n.substr(n.length-3);
		a.unshift(nn);
		n = n.substr(0,n.length-3);
	}
	if(n.length > 0) { a.unshift(n); }
	n = a.join(delimiter);
	amount = n;
	amount = minus + amount;
	return amount;
}