import sqlite3
from django.shortcuts import render


def favesellers_list(request):
    """Function to create an HTML report about which sellers are user favorites"""
    if request.method == 'GET':
        with sqlite.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()
            select_fave_sellers = """
                SELECT  user.first_name || ' ' || user.last_name AS seller_name
                FROM    bangazonapi_favorite AS fav
                JOIN    bangazonapi_customer AS cust ON cust.id=fav.seller_id
                JOIN    auth_user AS user ON cust.user_id=user.id
            """
            db_cursor.execute("""
                SELECT  user.first_name || '' || user.last_name AS customer_name,
                        fave_sellers.seller_name AS seller_name
                FROM    bangazonapi_favorite AS fav
                JOIN    bangazonapi_customer AS cust ON cust.id=fav.customer_id
                JOIN    auth_user AS user ON cust.user_id=user.id
                JOIN    (""" + select_fave_sellers + """) AS fave_sellers
                            ON fav.seller_id=fave_sellers.seller_id
            """)

            dataset = db_cursor.fetchall()

            customers = {}
            # iterate through each favorite
            for row in dataset:
                customer_name = row["customer_name"]
                seller_name = row["seller_name"]

                # each customer gets a dict in the customers dict
                if customer_name not in customers:
                    # each customer dict contains a "favorite_sellers" list
                    customers[customer_name] = {
                        "name": customer_name,
                        "favorite_sellers": [seller_name]
                    }
                else:
                    # if the customer's dict exists, just add to the faves list
                    customers[customer_name]["favorite_sellers"].append(
                        seller_name)

            # since we already have a name in each dict, we don't need the top level keys
            customer_list = customers.values()

            template = "users/customer_fave_sellers.html"
            context = {
                "customers_with_fave_sellers": customer_list
            }

            return render(request, template, context)
