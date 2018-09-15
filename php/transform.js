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