process.stdin.setEncoding("utf8");
const http = require('http');
const express = require("express");   /* Accessing express module */
const path = require("path");
const bodyParser = require("body-parser");
const portNumber = process.argv[2];
const app = express();  /* app is a request handler function */
app.set("views", path.resolve(__dirname, "templates"));
app.set("view engine", "ejs");
app.use(bodyParser.urlencoded({extended:false}));
console.log(`Web server is running at http://localhost:${portNumber}`);
process.stdout.write("Stop to shutdown the server: ");
let name1;


require("dotenv").config({ path: path.resolve(__dirname, 'credentials/.env') }) 


 const { MongoClient, ServerApiVersion } = require('mongodb');


process.stdin.on("readable", function () {
    let dataInput = process.stdin.read();
    if (dataInput !== null) {
        let command = dataInput.trim();
        if (command === "stop") {
            process.exit(0);
        }
    }
});

app.get("/", (request, response) => { 
    response.render("index", {});
});

app.listen(portNumber);