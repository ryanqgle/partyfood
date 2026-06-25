# partyfood

A CLI tool that helps party planners and caterers find recipes that accommodate their guests' dietary restrictions and estimates ingredient costs.

## Overview

When planning a party, guests often have differing diets, allergies, and restrictions that can make it hard for the party planner to choose food that everyone can eat. With our project, party planners would have a tool that allows them to get meal ideas that align with everyone’s different dietary restrictions, and it would also help them in their budget planning by generating AI-powered cost estimates based on recipe ingredients and attendee count.

## Features

- Search for recipes filtered by diet type and food intolerances
- Generate AI-powered cost estimates for recipes based on ingredients and attendee count
- Organize recipes by meal category (mains, sides, appetizers, desserts, drinks)
- Save events with their guest constraints and generated recipes
- Manage multiple events (birthday parties, weddings, etc.)

## Tech Stack

| Layer | Technology |
|---|---|
| Interface | CLI |
| Recipe data | [Spoonacular API](https://spoonacular.com/food-api) |
| Cost estimation | [Google Gemini API](https://ai.google.dev/gemini-api) |
| Storage | SQLite (local database) |

## Quick Start

See [Architecture](./Architecture.md) for system design, data flow, and database schema.

See [Setup](./Setup.md) for CLI walkthrough of how to set up this project and how to use it.

## Supported Diets

Paleo, Low FODMAP, Pescetarian, Gluten Free, Ketogenic, Vegetarian, Lacto-Vegetarian, Ovo-Vegetarian, Vegan, Primal, Whole30

## Supported Intolerances

Dairy, Egg, Gluten, Grain, Peanut, Seafood, Sesame, Shellfish, Soy, Sulfite, Tree Nut, Wheat

## Risk Considerations

The most critical risk is returning a recipe that does not conform to a user's restrictions (e.g. recommending a dish containing peanuts to someone with a peanut allergy). Success is defined as the tool consistently and correctly filtering recipes to match all specified constraints.
