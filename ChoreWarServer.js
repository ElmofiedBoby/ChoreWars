process.stdin.setEncoding("utf8");
import fetch from 'node-fetch';
import express from 'express';
import path from 'path';
import bodyParser from 'body-parser';
import { fileURLToPath } from 'url';
//const express = require("express");   /* Accessing express module */
//const path = require("path");
//const bodyParser = require("body-parser");
const portNumber = process.argv[2];
const __dirname = path.dirname(fileURLToPath(import.meta.url));
const app = express();  /* app is a request handler function */
app.set("views", path.resolve(__dirname, "templates"));
app.set("view engine", "ejs");
app.use(bodyParser.urlencoded({extended:false}));
app.use(express.static('static'))
console.log(`Web server is running at http://localhost:${portNumber}`);
process.stdout.write("stop to shutdown the server: ");
let name1;

class Task {
    constructor(description, points, frequency){
        this.description = description;
        this.points = points;
        this.frequency = frequency

    }
}

var taskArr = new Array()

function addNewTask(){

}

//require("dotenv").config({ path: path.resolve(__dirname, 'credentials/.env') }) 


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

    let variables = {
		valLink: "null",
		styleLoggedOut: "button-55",
		styleLoggedIn: "button-55-disabled",
        username: "null",
        valButton: "null"
	}

    response.render("index", variables);
});


app.get("/createTasks", (request, response) => { 
    const variables ={
        
    }
    response.render("createTasks", variables);

});

app.post("/createTasks", async (request, response) => { 
    
    let task_name = request.body.taskDescription;
    let task_points = request.body.pointsAmount;
    let task_freq = request.body.daysAmount;
    let task_start = new Date();
    let task_complete = false;

    let data = {
        "task_name": task_name,
        "task_description": null,
        "task_points": task_points,
        "task_freq": task_freq,
        "task_start": task_start,
        "task_complete": task_complete,
        "user_id": user_id
    }
    
    const variables = {
       /* taskDescription: request.body.taskDescription,
        pointAmount: request.body.pointAmount,
        daysAmount: request.body.daysAmount,*/
        tasks: taskArr
    };
    //taskArr.push(Task(taskDescription, pointAmount, daysAmount))
    response.render("tasks", variables); 
});

app.get("/leaderboard", (request, response) => { 
    const variables ={
        
    }
    response.render("leaderboard", variables);

});

app.get("/login", (request, response) => { 
    const variables ={
    }
    response.render("login", variables);

});

app.get("/signup", (request, response) => { 
    const variables ={
        
    }
    response.render("signup", variables);

});

app.get("/tasks", (request, response) => { 
    const variables ={
        
    }
    response.render("tasks", variables);

});

app.post("/login", (request, response) => {

    //const userData = '{ user_name: '+request.body.username+', user_password: '+request.body.password+' }';
    const userData = {
        user_name: request.body.username,
        user_password: request.body.password
    };

    fetch('http://localhost:5001/get/user/validate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(userData),
        })
        .then(response => {
        if (!response.ok) {
            throw new Error(response.status);
        }
        return response.json();
        })
        .then(data => {
        console.log(data);
        if(data.success === true) {
            let variables = {
                user_id: data.user_id
            }
            response.cookie('user_id', data.user_id);
            response.redirect('/tasks');
        }
        else {
            response.redirect('/');
        }
            
        })
        .catch(error => {
        console.error(error);
        });
})

app.listen(portNumber);