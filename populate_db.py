import os
import json
import psycopg2
from psycopg2.extras import execute_batch
from psycopg2.extras import Json

# --- Constants ---
BUSINESS_JSON_PATH = "data/business.json"
USER_JSON_PATH = "data/user.json"
REVIEW_JSON_PATH = "data/review.json"
TIP_JSON_PATH = "data/tip.json"
USERNAME = "seth" # replace with your Linux/psql username

def load_businesses(conn):
    print("Loading businesses...")

    insert_query = """
        INSERT INTO business (
            business_id, name, address, city, state, postal_code,
            latitude, longitude, stars, review_count, is_open,
            attributes, categories, hours, business_account_id
        ) VALUES (
            %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s,
            %s, %s, %s, %s
        )
    """

    data_to_insert = []

    with open(BUSINESS_JSON_PATH, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f):
            try:
                business = json.loads(line)

                # convert categories from string to list
                raw_categories = business.get("categories")
                if raw_categories:
                    categories_list = [cat.strip() for cat in raw_categories.split(",")]
                else:
                    categories_list = None  # will be inserted as NULL

                data_to_insert.append((
                    business.get("business_id"),
                    business.get("name"),
                    business.get("address"),
                    business.get("city"),
                    business.get("state"),
                    business.get("postal_code"),
                    business.get("latitude"),
                    business.get("longitude"),
                    business.get("stars"),
                    business.get("review_count"),
                    business.get("is_open"),
                    Json(business.get("attributes")),
                    categories_list,
                    Json(business.get("hours")),
                    None  # business_account_id is null for existing businesses
                ))

                # batch every 1000 lines
                if line_num > 0 and line_num % 1000 == 0:
                    execute_batch(conn.cursor(), insert_query, data_to_insert)
                    conn.commit()
                    data_to_insert.clear()
                    print(f"{line_num} businesses inserted...")

            except Exception as e:
                print(f"Error parsing line {line_num}: {e}")

    # insert any remaining records
    if data_to_insert:
        execute_batch(conn.cursor(), insert_query, data_to_insert)
        conn.commit()
        print(f"Final batch inserted: {len(data_to_insert)} businesses.")

    print("Finished loading businesses.")


def load_users(conn):
    print("Loading users...")

    insert_query = """
        INSERT INTO yelp_user (
            user_id, name, yelping_since,
            useful, funny, cool,
            compliment_useful, compliment_cool, compliment_funny,
            average_stars, review_count,
            username, password
        ) VALUES (
            %s, %s, %s,
            %s, %s, %s,
            %s, %s, %s,
            %s, %s,
            %s, %s
        )
    """

    data_to_insert = []

    with open(USER_JSON_PATH, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f):
            try:
                user = json.loads(line)

                data_to_insert.append((
                    user.get("user_id"),
                    user.get("name"),
                    user.get("yelping_since"),
                    user.get("useful"),
                    user.get("funny"),
                    user.get("cool"),
                    user.get("compliment_writer"),  # → compliment_useful
                    user.get("compliment_cool"),
                    user.get("compliment_funny"),
                    user.get("average_stars"),
                    user.get("review_count"),
                    None,  # username
                    None   # password
                ))

                if line_num > 0 and line_num % 1000 == 0:
                    execute_batch(conn.cursor(), insert_query, data_to_insert)
                    conn.commit()
                    data_to_insert.clear()
                    print(f"{line_num} users inserted...")

            except Exception as e:
                print(f"Error parsing user line {line_num}: {e}")

    # Final flush
    if data_to_insert:
        execute_batch(conn.cursor(), insert_query, data_to_insert)
        conn.commit()
        print(f"Final batch inserted: {len(data_to_insert)} users.")

    print("Finished loading users.")


def load_reviews(conn):
    print("Loading reviews...")

    insert_query = """
        INSERT INTO review (
            review_id, user_id, business_id,
            stars, useful, funny, cool,
            text, date
        ) VALUES (
            %s, %s, %s,
            %s, %s, %s, %s,
            %s, %s
        )
    """

    data_to_insert = []

    with open(REVIEW_JSON_PATH, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f):
            try:
                review = json.loads(line)

                data_to_insert.append((
                    review.get("review_id"),
                    review.get("user_id"),
                    review.get("business_id"),
                    review.get("stars"),
                    review.get("useful"),
                    review.get("funny"),
                    review.get("cool"),
                    review.get("text"),
                    review.get("date")
                ))

                if line_num > 0 and line_num % 1000 == 0:
                    execute_batch(conn.cursor(), insert_query, data_to_insert)
                    conn.commit()
                    data_to_insert.clear()
                    print(f"{line_num} reviews inserted...")

            except Exception as e:
                print(f"Error parsing review line {line_num}: {e}")

    # Final flush
    if data_to_insert:
        execute_batch(conn.cursor(), insert_query, data_to_insert)
        conn.commit()
        print(f"Final batch inserted: {len(data_to_insert)} reviews.")

    print("Finished loading reviews.")


def load_tips(conn):
    print("Loading tips...")

    insert_query = """
        INSERT INTO tip (
            user_id, business_id, text, date, praise_count
        ) VALUES (
            %s, %s, %s, %s, %s
        )
    """

    data_to_insert = []

    with open(TIP_JSON_PATH, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f):
            try:
                tip = json.loads(line)

                data_to_insert.append((
                    tip.get("user_id"),
                    tip.get("business_id"),
                    tip.get("text"),
                    tip.get("date"),
                    tip.get("compliment_count")  # → mapped to praise_count
                ))

                if line_num > 0 and line_num % 1000 == 0:
                    execute_batch(conn.cursor(), insert_query, data_to_insert)
                    conn.commit()
                    data_to_insert.clear()
                    print(f"{line_num} tips inserted...")

            except Exception as e:
                print(f"Error parsing tip line {line_num}: {e}")

    # Final flush
    if data_to_insert:
        execute_batch(conn.cursor(), insert_query, data_to_insert)
        conn.commit()
        print(f"Final batch inserted: {len(data_to_insert)} tips.")

    print("Finished loading tips.")


def main():
    try:
        conn = psycopg2.connect(
            dbname="yelpDB",
            user=USERNAME,         
            host="/tmp",             
            port=8888,                 
        )

        print("Connected to database successfully.")

        load_businesses(conn)
        load_users(conn)
        load_reviews(conn)
        load_tips(conn)

        conn.commit()
        print("All data loaded successfully.")

    except Exception as e:
        print("Error during database population:", e)

    finally:
        if conn:
            conn.close()
            print("Database connection closed.")

if __name__ == "__main__":
    main()

