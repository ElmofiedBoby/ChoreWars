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


require("dotenv").config({ path: path.resolve(__dirname, 'credentials/.env') }) 


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
    const variables = {
       /* taskDescription: request.body.taskDescription,
        pointAmount: request.body.pointAmount,
        daysAmount: request.body.daysAmount,*/
        tasks: request.body.taskDescription
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

app.listen(portNumber);