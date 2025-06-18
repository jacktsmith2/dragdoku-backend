import json
from datetime import datetime
from zoneinfo import ZoneInfo
from supabase import create_client

SUPABASE_URL = "https://ubnphrvwjzucdawtbmws.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVibnBocnZ3anp1Y2Rhd3RibXdzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTAyNzgxOTYsImV4cCI6MjA2NTg1NDE5Nn0.StVlYNhc95G7LPzeKzHprnTwY6R7DQ2sxJs8GdQryyA"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def validate_guess(row_idx, col_idx, queen_name):
    try:
        toronto_today = datetime.now(ZoneInfo("America/Toronto")).date().isoformat()

        # 1. Get today's grid from Supabase Storage JSON
        filename = f"grid_{toronto_today}.json"
        res = supabase.storage.from_("grids").download(filename)
        if not res:
            return False, "❌ No grid found for today.", None
        grid_json = res.decode('utf-8')
        grid = json.loads(grid_json)

        row_sql_list = grid.get("row_sql")
        col_sql_list = grid.get("col_sql")

        if row_sql_list is None or col_sql_list is None:
            return False, "❌ Grid data malformed.", None

        if row_idx >= len(row_sql_list) or col_idx >= len(col_sql_list):
            return False, "❌ Invalid row or column index.", None

        row_sql = row_sql_list[row_idx]
        col_sql = col_sql_list[col_idx]

        # 2. Validate queen with filter against Supabase Postgres
        # Supabase client doesn't support raw SQL queries directly,
        # so you must implement Postgres RPC or predefine filters.
        # Here’s a simple placeholder that fetches queen matching name,
        # then you can implement server-side filtering or RPC for criteria

        response = supabase.table("queens") \
            .select("image") \
            .eq("queen_name", queen_name) \
            .execute()

        if response.error or len(response.data) == 0:
            return False, "❌ Queen not found.", None

        # NOTE: You must implement logic to check if this queen matches row_sql AND col_sql.
        # Since Supabase-py doesn't run raw SQL, consider:
        # - Creating a Postgres function to check criteria (recommended)
        # - Or fetch queen's full data and apply criteria filtering in Python (less efficient)

        # Placeholder: if queen exists, accept as valid (adjust as needed)
        image_url = response.data[0].get("image")

        # Incomplete validation - refine with your RPC or filtering
        return True, "✅ Correct! (validation placeholder)", image_url

    except Exception as e:
        print("❌ Validation error:", e)
        return False, "❌ Internal error.", None
