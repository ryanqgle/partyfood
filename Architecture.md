# Architecture

## Data Flow

```
User Input (CLI)
      │
      ▼
  Backend / App Logic
      │
      ├──► Spoonacular API  ──► Recipe results (filtered by diet, intolerances, ingredients)
      │
      └──► Kroger API  ──► Ingredient pricing
      │
      ▼
  Normalize & Combine Data
      │
      ▼
  CLI Output (recipes + cost estimates)
      │
      ▼
  SQLite Database  ◄──► Save recipes to event (optional)
```

### Step-by-Step

1. App prompts user for to do either:
   1. [View and Edit Events](#view-and-edit-events)
   2. [Create New Event](#create-new-event)
   3. [Generate Recipes](#generate-recipes)
2. User makes selections via numbered/lettered CLI menus.
3. Backend stores inputs and sends a `GET` request to the **Spoonacular API** with `diet`, `intolerances`, and ingredient parameters.
4. Using Spoonacular results, backend sends a `GET` request to the **Kroger API** to fetch ingredient pricing.
5. Backend normalizes and merges data, then displays categorized recipes with cost breakdowns.
6. User may optionally save chosen recipes and events.
   
### View and Edit Events

Lets users do the following:
- Add/remove diets
- Add/remove intolerances
- Add/remove available ingredients
- Set/update attendee count
- Generate recipes
- Remove recipe
- Go back

Events should look like the [example outputs](#example-events)
   
### Create New Event

   1. Enter # of attendees: `user input`.
   2. What ingredients does the user already have = (besides pantry items like salt, flour, water, etc.): `user input`.
   3. Prompts user to choose a diet from the [list of supported diets](README.md#supported-diets) or to go back.
   4. Prompts user to choose any intolerances from the [list of supported intolerances](README.md#supported-intolerances) or to go back.

Events should look like the [example outputs](#example-events)
   
### Generate Recipes

Prompts the user to select an event to generate recipes for, then generates the recipe.

## External APIs

### Spoonacular

- **Endpoint used:** [`/recipes/complexSearch`](https://spoonacular.com/food-api/docs#Search-Recipes-Complex)
  - Query params: `diet`, `intolerances`, `includeIngredients`, `type`
- **Optional:** [`/recipes/{id}/analyzedInstructions`](https://spoonacular.com/food-api/docs#Get-Analyzed-Recipe-Instructions) — for displaying step-by-step cooking instructions
- **Rate limit:** 150 requests/day (free tier)

### Kroger

- **Endpoint used:** [Product API](https://developer.kroger.com/api-products/api/product-api-partner)
  - Used to look up ingredient prices by name

## Database Schema

The local SQLite database stores **events** and their associated data.

### `events` table

| Field | Type | Description |
|---|---|---|
| `id` | INTEGER (PRIMARY KEY) | Auto-incremented event ID |
| `name` | TEXT | Name of the event (e.g. "Mia's 1st Birthday") |
| `attendee_count` | INTEGER | Number of guests |

### `event_diets` table

| Field | Type | Description |
|---|---|---|
| `event_id` | INTEGER (FOREIGN KEY) | References `events.id` |
| `diet` | TEXT | Diet name (e.g. `"pescetarian"`, `"gluten-free"`) |

### `event_intolerances` table

| Field | Type | Description |
|---|---|---|
| `event_id` | INTEGER (FOREIGN KEY) | References `events.id` |
| `intolerance` | TEXT | Intolerance name (e.g. `"dairy"`, `"peanut"`) |

### `ingredients` table

| Field | Type | Description |
|---|---|---|
| `event_id` | INTEGER (FOREIGN KEY) | References `events.id` |
| `event_ingredients` | TEXT | List of available ingredients (e.g. 'eggs,butter,peanuts') |

### `event_recipes` table

| Field | Type | Description |
|---|---|---|
| `event_id` | INTEGER (FOREIGN KEY) | References `events.id` |
| `recipe_id` | TEXT | Spoonacular recipe ID |
| `recipe_name` | TEXT | Display name |
| `category` | TEXT | e.g. `"main"`, `"dessert"`, `"drink"` |
| `estimated_cost` | REAL | Total ingredient cost from Kroger |

## Example Events

### Mia's 1st Birthday Party
- **Attendees:** 7
- **Available ingredients:** Strawberries
- **Diets:** Pescetarian, Gluten-Free
- **Intolerances:** Dairy

### Wedding Reception
- **Attendees:** 250
- **Available ingredients:** Ice cream, cherries
- **Diets:** Ketogenic, Whole30, Vegetarian
- **Intolerances:** Wheat, Egg, Peanut, Soy
