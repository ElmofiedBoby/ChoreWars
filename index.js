const { Sequelize } = require('sequelize');
const { Dialects } = require('sequelize-cockroachdb');
const express = require('express');


// Create an instance of the Express app
const app = express()

// Create an instance of the Sequelize ORM
const sequelize = new Sequelize('choreWars', 'chorewarrior', 'k8k8_NFNYD1nZfvVdePXBg', {
  dialect: 'postgres',
  dialectModule: Dialects.postgres,
  host: 'db-chorewars-01-10084.7tt.cockroachlabs.cloud',
  port: 26257,
  dialectOptions: {
    ssl: {
      rejectUnauthorized: false,
    },
  },
});

// Define a Task model
const Task = sequelize.define('Task', {
  title: {
    type: Sequelize.STRING,
    allowNull: false,
  },
  description: {
    type: Sequelize.TEXT,
    allowNull: false,
  },
  completed: {
    type: Sequelize.BOOLEAN,
    defaultValue: false,
  },
});

// Sync the model with the database and start the server
async function main() {
  try {
    await sequelize.authenticate();
    console.log('Connection has been established successfully.');

    // Sync the model with the database
    await Task.sync({ force: true });
    console.log('Task model synced with database.');

    // Start the server on port 3000
    app.listen(3000, () => {
      console.log('Server is listening on port 3000');
    });
  } catch (error) {
    console.error('Unable to connect to the database:', error);
  }
}

// Call the main function to start the server
main();