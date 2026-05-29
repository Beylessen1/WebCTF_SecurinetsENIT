<?php

if (!isset($_FILES['file'])) {
    die("No file uploaded.");
}

$upload_dir = "uploads/";
$file_name = basename($_FILES["file"]["name"]);
$target = $upload_dir . $file_name;

// INTENTIONAL VULNERABILITY: raw file upload
if (move_uploaded_file($_FILES["file"]["tmp_name"], $target)) {
    echo "Uploaded successfully!<br>";
    echo "File: <a href='uploads/$file_name'>uploads/$file_name</a>";
    echo "<br><br>Tip: Files execute if they are PHP 😉";
} else {
    echo "Upload failed.";
}
