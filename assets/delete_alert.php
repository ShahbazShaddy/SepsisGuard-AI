<?php
header('Content-Type: application/json');

// Read the POST data
$input = file_get_contents("php://input");
$data = json_decode($input, true);

// Check if index is set
if (!isset($data['index'])) {
    echo json_encode(['success' => false, 'message' => 'Index not specified']);
    exit;
}

$index = intval($data['index']);

// Path to the CSV file
$csvFile = './assets/data.csv';

// Read the CSV file
if (($handle = fopen($csvFile, 'r')) === false) {
    echo json_encode(['success' => false, 'message' => 'Failed to open CSV file']);
    exit;
}

// Parse CSV
$rows = [];
$header = fgetcsv($handle); // Read the header row
while (($row = fgetcsv($handle)) !== false) {
    $rows[] = $row;
}
fclose($handle);

// Remove the specified row
if (isset($rows[$index])) {
    unset($rows[$index]);
}

// Re-index array
$rows = array_values($rows);

// Write the updated data back to the CSV file
if (($handle = fopen($csvFile, 'w')) === false) {
    echo json_encode(['success' => false, 'message' => 'Failed to open CSV file for writing']);
    exit;
}

// Write header
fputcsv($handle, $header);

// Write data
foreach ($rows as $row) {
    fputcsv($handle, $row);
}
fclose($handle);

echo json_encode(['success' => true]);
