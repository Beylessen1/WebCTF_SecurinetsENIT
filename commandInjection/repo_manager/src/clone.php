<?php

$cmd = $_GET['cmd'];

echo "<h2>Cloning Repository...</h2>";
echo "<pre>";

system("git clone " . $cmd);

echo "</pre>";

?>
