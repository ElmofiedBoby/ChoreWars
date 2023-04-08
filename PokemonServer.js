import Pokedex from 'pokedex-promise-v2';
import express from 'express';
import bodyParser from 'body-parser';
import path from 'path';
import dotenv from 'dotenv';
import { MongoClient, ServerApiVersion } from 'mongodb';
import multer from 'multer';
import fs from 'fs';

/* Port Arguments */
if (process.argv.length !== 3) {
	console.log(">:(\nUsage: pokemonFinderServer.js portNumber");
	process.exit(1);
}
else {
	var portNumber = process.argv[2];
}

/* Basic Setup */
const __dirname = path.resolve(path.dirname(''));
dotenv.config({ path: path.resolve(__dirname, '.env') });
const userName = process.env.MONGO_DB_USERNAME;
const password = process.env.MONGO_DB_PASSWORD;
const databaseAndCollection = { db: process.env.MONGO_DB_NAME, user_collection: process.env.MONGO_COLLECTION_USERS, matches_collection: process.env.MONGO_COLLECTION_MATCHES };
const uri = `mongodb+srv://${userName}:${password}@cluster0.l9m35rn.mongodb.net/${process.env.MONGO_DB_NAME}?retryWrites=true&w=majority`;
const mongoclient = new MongoClient(uri, { useNewUrlParser: true, useUnifiedTopology: true, serverApi: ServerApiVersion.v1 });
const users = mongoclient.db(databaseAndCollection.db).collection(databaseAndCollection.user_collection);
const matches = mongoclient.db(databaseAndCollection.db).collection(databaseAndCollection.matches_collection);
const P = new Pokedex();

let loggedin = false;
let username = null;
let profileType = null;

/* App Setup */
const app = express();
app.use(bodyParser.urlencoded({ extended: false }));
app.use(express.static('static'));
app.set("views", path.resolve(__dirname, "templates"));
app.set("view engine", "ejs");

/* App Endpoints */
app.use('/static', express.static(__dirname + '/public'));

app.get("/logout", (request,response) => {
	loggedin = false;
	username = null;
	let variables = {
		username: "no one",
		styleLoggedOut: "button-55",
		styleLoggedIn: "button-55-disabled"
	}
	response.render("index", variables);
});

app.get("/", (request, response) => {
	if(username == null) {
		let variables = {
			username: "no one",
			styleLoggedOut: "button-55",
			styleLoggedIn: "button-55-disabled"
		}
		response.render("index", variables);
	}
	else {
		let variables = {
			username: username,
			styleLoggedOut: "button-55-disabled",
			styleLoggedIn: "button-55"
		}
		response.render("index", variables);
	}
});

app.post("/signin", (request, response) => {
	mongoclient.connect(async err => {
		let result = await users.findOne({username: request.body.signin});
		if(result) {
			loggedin = true;
			username = request.body.signin;
			const variables = {
				username: username,
				styleLoggedOut: "button-55-disabled",
				styleLoggedIn: "button-55"
			}
			response.render("index", variables);
		}
		else {
			console.log("User does not exist!");
			loggedin = false;
			username = null;
			const variables = {
				username: "no one",
				styleLoggedOut: "button-55",
				styleLoggedIn: "button-55-disabled"
			}
			response.render("index", variables);
		}
		await mongoclient.close();
	})

})




	




/* Functions */


function clearDB() {
	console.log("Clearing databases and profile pictures");
	mongoclient.connect(async err => {
		await users.deleteMany();
		await matches.deleteMany();
		await mongoclient.close();
	});
	fs.rmdir('static/pfp', {recursive:true, force:true}, (err) => {
		if(err) {
			return console.log("folder deletion error",err);
		}
		fs.mkdir('static/pfp', {}, (err) => {
			if(err) {
				return console.log("folder creation error",err);
			}
		});
	});
}


/* Server Console Logic */
var dataInput = '';
clearDB(); //need to change method to work with cock
app.listen(portNumber);
console.log(`Web server started and running at http://localhost:${portNumber}`);
process.stdin.setEncoding("utf8");
process.stdout.write("^_^: ")
process.stdin.on('readable', () => {
	while ((dataInput = process.stdin.read()) !== null) {
		let command = dataInput.trim();
		if (command === "stop") {
			console.log("Shutting down the server");
			process.exit(0);
		}
		else if(command == "clear") {
			clearDB();
		}
		else {
			console.log(`Invalid command: ${command}`);
		}
		process.stdout.write("^_^: ");
	}
});