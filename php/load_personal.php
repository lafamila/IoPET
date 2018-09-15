<?php

    include_once('config.php');
    $pet_id = $_POST['pet_id'];
    $query = "SELECT * FROM `pet` WHERE `PET_ID` = $pet_id";
    
    print query($query, true, true);
?>