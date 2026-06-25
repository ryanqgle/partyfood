# Setup

A quick guide to get **partyfood** running locally.

## Prerequisites

- API keys for [Spoonacular](https://spoonacular.com/food-api) (recipe data). The free
  Spoonacular tier (150 requests/day) is enough to try the app.
- API key for Google Gemini (AI-powered cost estimation)

## 1. Clone and enter the project

```bash
git clone https://github.com/ryanqgle/partyfood.git
cd partyfood
```

## 2. Create a virtual environment (recommended)

```bash
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
```

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

This installs SQLAlchemy, requests, and python-dotenv.

## 4. Configure your API keys

Copy the example env file and fill in your keys:

```bash
cp .env.example .env
```

Then edit `.env` and replace the placeholder values:

```
SPOONACULAR_KEY=your_spoonacular_key
GEMINI_API_KEY=your_gemini_api_key
```

Leave the `*_BASE_URL` lines as-is.

## 5. Run the app

```bash
python3 main.py
```

On first launch the app creates a local SQLite database (`food.db`) from
`storage/schema.sql` automatically, so no manual database setup needed. The
database starts empty; create your first event from the main menu.

## Using the CLI

You navigate by typing the letter next to an option, then pressing Enter.

- **Create New Event** — set a name, attendee count, ingredients you already
  have, diets, and intolerances, then **Save Event** to persist it.
- **View and Edit Events** — list events, choose one, and edit it. Edits
  (diets, intolerances, ingredients, attendee count) save to the database
  immediately.
- **Generate Recipes** — from an event's Edit menu, fetches recipes from
  Spoonacular that match the event's diets and intolerances and prints them by
  category (main course, appetizer, dessert).
- **Generate Price Estimate** - from an event's menu, fetches recipes
  associated with the event and uses AI to create a price estimate which
  corresponds with the amount of expected attendees.

See [Architecture.md](./Architecture.md) for the data flow and database schema.
