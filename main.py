from fastapi import FastAPI, Query
import pandas as pd
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load correct sheet (you already fixed this part)
df = pd.read_excel("products.xlsx", sheet_name="Saleable")

# Clean columns
df.columns = df.columns.str.strip()

# ✅ FIX NAN ISSUE
df = df.fillna("")

print("Columns:", df.columns.tolist())

@app.get("/search")
def search_products(q: str = Query("")):
    if not q:
        return []

    result = df[
        df['Item Name'].astype(str).str.contains(q, case=False, na=False) |
        df['Brand'].astype(str).str.contains(q, case=False, na=False) |
        df['UPC'].astype(str).str.contains(q, case=False, na=False)
    ].head(50)

    # ✅ EXTRA SAFETY (recommended)
    result = result.fillna("")

    return result.to_dict(orient="records")