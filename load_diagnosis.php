<?php

    include_once('config.php');
    $pet_id = $_POST['pet_id'];
    $hospt_id = $_POST['hospt_id'];
    $query = "SELECT * FROM `diagnosis` WHERE `PET_ID` = $pet_id AND `HOSPITAL_ID` = $hospt_id";
    
    print query($query, false, true);
?>