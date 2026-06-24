/*
    storage/schema.sql

    This SQL file is used to create the database table structure.
    There will be multiples tables in order to organize and clearly outline the use of each item that gets stored into the database.
*/

/* Declare which database that we will put the tables in. */

/* The overarching list of events. */
CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY,
    event_name TEXT NOT NULL DEFAULT 'party',
    attendee_count INTEGER
);

/* If the event does not have any dietary restrictions, then the diets attribute may be null. */
CREATE TABLE IF NOT EXISTS event_diets (
    event_id INTEGER REFERENCES events(id),
    diet TEXT
);

/* If the event does not have any intolerances, then the intolerances attribute may be null. */
CREATE TABLE IF NOT EXISTS event_intolerances (
    event_id INTEGER REFERENCES events(id),
    intolerance TEXT
);

/* Table of ingredients that the user already has. May be null if the user has no ingredients. */
CREATE TABLE IF NOT EXISTS ingredients (
    event_id INTEGER REFERENCES events(id),
    event_ingredients TEXT
);

/* Table of recipes per their event id. */
CREATE TABLE IF NOT EXISTS event_recipes (
    event_id INTEGER REFERENCES events(id),
    recipe_id TEXT NOT NULL,
    recipe_name TEXT NOT NULL,
    category TEXT NOT NULL,
    estimated_cost REAL
);

/* Dummy data used for testing */
INSERT INTO events (event_name, attendee_count) VALUES ('Birthday Party', 20);
INSERT INTO events (event_name, attendee_count) VALUES ('Wedding Reception', 100);
INSERT INTO events (event_name, attendee_count) VALUES ('Corporate Event', 50);

/* event data for event 1: Birthday Party */ 
INSERT INTO event_diets (event_id, diet) VALUES (1, 'Vegetarian');
INSERT INTO event_intolerances (event_id, intolerance) VALUES (1, 'Egg');

/* event data for event 2: Wedding Reception */
INSERT INTO event_diets (event_id, diet) VALUES (2, 'Vegan');
INSERT INTO event_intolerances (event_id, intolerance) VALUES (2, 'Peanut');
INSERT INTO ingredients (event_id, event_ingredients) VALUES (2, 'tomatoes,onions,garlic');

/* event data for event 3: Corporate Event */
INSERT INTO event_diets (event_id, diet) VALUES (3, 'Gluten Free');
INSERT INTO event_intolerances (event_id, intolerance) VALUES (3, 'Dairy');
INSERT INTO ingredients (event_id, event_ingredients) VALUES (3, 'chicken,rice,broccoli');
