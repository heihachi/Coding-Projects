<?php

function write($id, $data)
{
    $file = "/var/www/cache/transfers/transfer.".$id.".pdump";
    $fp = fopen($file, 'a') or die("Error Writing to file");
    fwrite($fp, $data);
    fwrite("\n");
    fclose($fp);
}
function start()
{
    //write some stuff that may be required by the server
    write(1,"IMPORTANT NOTE: THIS DUMPFILE IS MADE FOR USE WITH THE 'PDUMP' COMMAND ONLY - EITHER THROUGH INGAME CHAT OR ON CONSOLE!");
    write(1,"IMPORTANT NOTE: DO NOT apply it directly - it will irreversibly DAMAGE and CORRUPT your database! You have been warned!");
    write(1,"\n");

}

function characters()
{
    //write the characters data
    write(1,"INSERT INTO `characters` VALUES (guid, accountid, name, race, class, gender, level, xp, money, playerBytes, playerBytes2, playerflags, position_x, position_y, position_z, map, instance_id, instance_mode_mask, orientation, taximask, online, cinematic, totaltime, leveltime, logout_time, is_logout_resting, rest_bonus, resettalents_cost, resettalents_time, trans_x, trans_y, trans_z, trans_o, transguid, extra_flags, stable_slots, at_login, zone, death_expire_time, taxi_path, arenaPoints, totalHonorPoints, todayHonorPoints, yesterdayHonorPoints, totalKills, todayKills, yesterdayKills, chosenTitle, knownCurrencies, watchedFaction, drunk, health, power1, power2, power3, power4, power5, power6, power7, latency, speccount, activespec, exploredzones, equipmentCache, ammoid, knownTitles, actionBars, grantableLevels, deleteInfos_Account, deleteInfos_Name, deleteDate);");
}

function character_achievement()
{
    //write the characters achievements
    write(1,"INSERT INTO `character_achievement` VALUES (guid, achievement, date);");
}

function character_inventory()
{
    //write the characters inventory
    write(1,"INSERT INTO `character_inventory` VALUES (guid, bag, slot, item);");
}

function character_reputation()
{
    //write the chracters rep data
    write(1,"");
}

function character_skills()
{
    //set up the profession skills
}

function character_spell()
{
    //add a few character spells
}

function item_instance()
{
    //finalize the inventory
}
?>