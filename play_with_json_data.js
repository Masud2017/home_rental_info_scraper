"use strict"
var json_data_url = "https://firestore.googleapis.com/v1/projects/home-rental-info/databases/(default)/documents/home_list/D1QiZHn7uOZY3lCSJ6eD";
var res = await  fetch(json_data_url).then(data => data.json())
var json_string_data = res.fields.data.stringValue

var json_data = JSON.parse(json_string_data);

console.log(json_data);