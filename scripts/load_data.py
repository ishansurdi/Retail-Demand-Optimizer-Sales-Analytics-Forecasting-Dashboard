# load_data.py
import pandas as pd
import mysql.connector
from mysql.connector import Error

# ===============================
# DB CONFIG
# ===============================
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "123456789",   # change this
    "database": "retail_optimizer"
}



# ===============================
# HELPER: connect to DB
# ===============================
def get_connection():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Error as e:
        print("❌ DB Connection error:", e)
        return None

# ===============================
# LOAD SUPERSTORE DATA
# ===============================
def load_superstore(csv_path):
    

    print("📥 Loading Superstore dataset...")
    df = pd.read_csv(csv_path, encoding="latin1")
    df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce", dayfirst=False).dt.strftime("%Y-%m-%d")
    df["Ship Date"]  = pd.to_datetime(df["Ship Date"], errors="coerce", dayfirst=False).dt.strftime("%Y-%m-%d")

    conn = get_connection()
    if not conn: return
    cursor = conn.cursor()

    insert_query = """
    INSERT INTO superstore_sales (
        row_id, order_id, order_date, ship_date, ship_mode, customer_id, customer_name,
        segment, country, city, state, postal_code, region, product_id, category,
        sub_category, product_name, sales, quantity, discount, profit
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

    for idx, row in df.iterrows():
        try:
            cursor.execute(insert_query, (
            int(idx + 1), 
            row["Order ID"],
            row["Order Date"] if pd.notna(row["Order Date"]) else None,
            row["Ship Date"] if pd.notna(row["Ship Date"]) else None,
            row["Ship Mode"],
            row["Customer ID"],
            row["Customer Name"],
            row["Segment"],
            row["Country"],
            row["City"],
            row["State"],
            str(row["Postal Code"]) if not pd.isna(row["Postal Code"]) else None,  # ensure string
            row["Region"],
            row["Product ID"],
            row["Category"],
            row["Sub-Category"],
            row["Product Name"],
            float(row["Sales"]),
            int(row["Quantity"]),
            float(row["Discount"]),
            float(row["Profit"]),
            ))
        except Exception as e:
            print(f"⚠️ Error inserting row {row['Order ID']}: {e}")

    conn.commit()
    cursor.close()
    conn.close()
    print("✅ Superstore data loaded.")

# ===============================
# LOAD WALMART DATA
# ===============================
def load_walmart_stores(csv_path):
    print("📥 Loading Walmart Stores...")
    df = pd.read_csv(csv_path)
    conn = get_connection()
    if not conn: return
    cursor = conn.cursor()

    insert_query = "INSERT INTO walmart_stores (store, type, size) VALUES (%s, %s, %s)"
    for _, row in df.iterrows():
        cursor.execute(insert_query, (int(row["Store"]), row["Type"], int(row["Size"])))
    
    conn.commit()
    cursor.close()
    conn.close()
    print("✅ Walmart stores loaded.")

def load_walmart_features(csv_path):
    print("📥 Loading Walmart Features...")
    df = pd.read_csv(csv_path)
    conn = get_connection()
    if not conn: return
    cursor = conn.cursor()

    insert_query = """
        INSERT INTO walmart_features 
        (store, date, temperature, fuel_price, markdown1, markdown2, markdown3, markdown4, markdown5, cpi, unemployment, is_holiday)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    for _, row in df.iterrows():
        try:
            cursor.execute(insert_query, (
                int(row["Store"]),
                pd.to_datetime(row["Date"]).strftime("%Y-%m-%d"),
                float(row["Temperature"]) if pd.notna(row["Temperature"]) else None,
                float(row["Fuel_Price"]) if pd.notna(row["Fuel_Price"]) else None,
                float(row["MarkDown1"]) if pd.notna(row["MarkDown1"]) else None,
                float(row["MarkDown2"]) if pd.notna(row["MarkDown2"]) else None,
                float(row["MarkDown3"]) if pd.notna(row["MarkDown3"]) else None,
                float(row["MarkDown4"]) if pd.notna(row["MarkDown4"]) else None,
                float(row["MarkDown5"]) if pd.notna(row["MarkDown5"]) else None,
                float(row["CPI"]) if pd.notna(row["CPI"]) else None,
                float(row["Unemployment"]) if pd.notna(row["Unemployment"]) else None,
                bool(row["IsHoliday"])
            ))
        except Exception as e:
            print(f"⚠️ Error inserting Walmart feature row: {e}")
    
    conn.commit()
    cursor.close()
    conn.close()
    print("✅ Walmart features loaded.")

def load_walmart_sales_train(csv_path):
    print("📥 Loading Walmart Train Sales...")
    df = pd.read_csv(csv_path)

    # Preprocess date safely
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    # Drop rows where date is NaT
    df = df.dropna(subset=["Date"])

    # Format as YYYY-MM-DD for MySQL
    df["Date"] = df["Date"].dt.strftime("%Y-%m-%d")

    # Convert dataframe into list of tuples for bulk insert
    data = [
        (
            int(row["Store"]),
            int(row["Dept"]),
            row["Date"],
            float(row["Weekly_Sales"]),
            bool(row["IsHoliday"])
        )
        for _, row in df.iterrows()
    ]

    conn = get_connection()
    if not conn:
        return
    cursor = conn.cursor()

    insert_query = """
        INSERT INTO walmart_train (store, dept, date, weekly_sales, is_holiday)
        VALUES (%s, %s, %s, %s, %s)
    """

    try:
        cursor.executemany(insert_query, data)   # 🚀 bulk insert
        conn.commit()
        print(f"✅ Walmart train sales loaded ({len(data)} rows).")
    except Exception as e:
        print("❌ Error bulk inserting:", e)
    finally:
        cursor.close()
        conn.close()


def load_walmart_sales_test(csv_path):
    print("📥 Loading Walmart Test Sales...")
    df = pd.read_csv(csv_path)
    conn = get_connection()
    if not conn: return
    cursor = conn.cursor()

    insert_query = "INSERT INTO walmart_test (store, dept, date, is_holiday) VALUES (%s, %s, %s, %s)"
    for _, row in df.iterrows():
        cursor.execute(insert_query, (
            int(row["Store"]),
            int(row["Dept"]),
            pd.to_datetime(row["Date"]).strftime("%Y-%m-%d"),
            bool(row["IsHoliday"])
        ))
    
    conn.commit()
    cursor.close()
    conn.close()
    print("✅ Walmart test sales loaded.")

# ===============================
# MAIN
# ===============================
if __name__ == "__main__":
    # Superstore
    load_superstore("data/superstore.csv")

    # Walmart
    load_walmart_stores("data/stores.csv")
    load_walmart_features("data/features.csv")
    load_walmart_sales_train("data/train.csv")
    load_walmart_sales_test("data/test.csv")
