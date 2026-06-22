# partyfood

A CLI tool that helps party planners and caterers find recipes that accommodate their guests' dietary restrictions and estimates ingredient costs.

## Overview

When planning a party or catering event, guests often have differing diets, allergies, and restrictions that make it difficult to choose food everyone can eat. **partyfood** solves this by letting planners input their attendees' dietary constraints and available ingredients, then surfacing compatible recipes with real grocery pricing.

## Features

- Search for recipes filtered by diet type and food intolerances
- Input available ingredients to minimize what you need to buy
- Get cost estimates per recipe using live grocery data
- Organize recipes by meal category (mains, sides, appetizers, desserts, drinks)
- Save events with their guest constraints and generated recipes
- Manage multiple events (birthday parties, weddings, etc.)

## Tech Stack

| Layer | Technology |
|---|---|
| Interface | CLI |
| Recipe data | [Spoonacular API](https://spoonacular.com/food-api) |
| Grocery pricing | [Kroger API](https://developer.kroger.com/api-products/api/product-api-partner) |
| Storage | SQLite (local database) |

## Quick Start

See [Architecture](./ARCHITECTURE.md) for system design, data flow, and database schema.

See [Setup](./Setup.md) for CLI walkthrough of how to set up this project and how to use it.

## Supported Diets

Paleo, Low FODMAP, Pescetarian, Gluten Free, Ketogenic, Vegetarian, Lacto-Vegetarian, Ovo-Vegetarian, Vegan, Primal, Whole30

## Supported Intolerances

Dairy, Egg, Gluten, Grain, Peanut, Seafood, Sesame, Shellfish, Soy, Sulfite, Tree Nut, Wheat

## Risk Considerations

The most critical risk is returning a recipe that does not conform to a user's restrictions (e.g. recommending a dish containing peanuts to someone with a peanut allergy). Success is defined as the tool **consistently and correctly** filtering recipes to match all specified constraints.
