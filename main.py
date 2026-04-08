from fastapi import FastAPI, Query
import pandas as pd
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Load Excel (both sheets)
df_saleable = pd.read_excel("products.xlsx", sheet_name="Saleable")
df_non = pd.read_excel("products.xlsx", sheet_name="Non Saleable")

# ✅ Clean + add sheet type
def prepare_df(df, label):
    df.columns = df.columns.str.strip()
    df = df.fillna("")
    df["sheet_type"] = label
    return df

df_saleable = prepare_df(df_saleable, "Saleable")
df_non = prepare_df(df_non, "Non Saleable")

# ✅ Combine
df = pd.concat([df_saleable, df_non], ignore_index=True)

print("Columns:", df.columns.tolist())

# ✅ Root (for testing)
@app.get("/")
def home():
    return {"message": "API is working 🚀"}

# ✅ Search API
@app.get("/search")
def search_products(q: str = Query("")):
    if not q:
        return []

    result = df[
        df['Item Name'].astype(str).str.contains(q, case=False, na=False) |
        df['Brand'].astype(str).str.contains(q, case=False, na=False) |
        df['UPC'].astype(str).str.contains(q, case=False, na=False)
    ].head(50)

    result = result.fillna("")

    return result.to_dict(orient="records")