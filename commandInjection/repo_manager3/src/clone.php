<?php

$cmd = $_GET['cmd'] ?? ""; 
/* ${IFS} */ 

if (preg_match('/\s/', $cmd)) {
    die("Spaces are not allowed!");
}


echo "<h2>Cloning Repository...</h2>";
echo "<pre>";

system("git clone " . $cmd);

echo "</pre>";

?>

