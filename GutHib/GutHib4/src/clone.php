<?php

$cmd = $_GET['cmd'];

echo "<h2>Cloning Repository...</h2>";
echo "<pre>";

system("git clone " . $cmd . " > /dev/null 2>&1");

echo "</pre>";

?>
