import os
import webbrowser
from json import JSONDecodeError
from typing import List, TypedDict
from uuid import UUID

import requests
import typer

app = typer.Typer()

api_token = os.getenv("API_TOKEN")
headers = {"Authorization": f"Bearer {api_token}"}
ngrok_url = os.getenv("NGROK_URL", "https://api.useharp.com")


def check_api_token():
    if api_token is None:
        typer.echo(
            "API_TOKEN is not set. Please set your API token in the environment variables."
        )
        raise SystemExit


class Product(TypedDict):
    product_id: str
    quantity: int


@app.command()
def add_payment_method():
    check_api_token()
    typer.echo("Let's add a new payment method.")

    # Let's assume your FastAPI server is running locally on port 8000
    fastapi_url = os.getenv("FASTAPI_URL", ngrok_url)
    ### Add prefix after localhost
    request_url = f"{fastapi_url}/v1/buyer/create-checkout-session"

    # Request to generate a new Stripe Payment Method
    response = requests.post(request_url, headers=headers)
    if response.status_code == 200:
        response_json = response.json()

        stripe_payment_url = response_json["data"]

        # Open the Stripe Checkout page
        webbrowser.open(stripe_payment_url)

        # Once the user completes the payment on the Stripe Checkout page, Stripe will redirect them to your specified return_url (you will need to set this up on your FastAPI backend).
        # On the return page, you can retrieve the PaymentMethod ID from the URL parameters and send it back to the FastAPI backend to associate it with the user and save it in the database.
    else:
        typer.echo(response.status_code)
        typer.echo(
            "Something went wrong. It was reported to the devs. Slack us if you need help."
        )


@app.command()
def seller_connect():
    check_api_token()
    typer.echo("Let's connect your shopify store to harp.")

    # Let's assume your FastAPI server is running locally on port 8000
    fastapi_url = os.getenv("FASTAPI_URL", ngrok_url)
    ### Add prefix after localhost
    request_url = f"{fastapi_url}/v1/seller/stores/register/shopify/redirect"

    # Prompt user for shopify store name
    store_name = None
    while store_name is None:
        store_id_str = typer.prompt("Enter the Shopify store name")
        store_name = store_id_str

    # build request body

    request_body = {"shop_name": store_name, "origin_url": request_url}
    response = requests.post(request_url, json=request_body, headers=headers)
    if response.status_code == 200:
        response_json = response.json()

        auth_url = response_json["data"]["auth_url"]
        typer.echo(auth_url)

        # Open the Shopify Oauth connect
        # webbrowser.open(auth_url)

    else:
        typer.echo(response.status_code)
        typer.echo(
            "Something went wrong. It was reported to the devs. Slack us if you need help."
        )


@app.command()
def order():
    check_api_token()
    typer.echo("Let's create a new order.")

    # Prompt user for each field
    store_id = None
    store_id_str: str = ""
    while store_id is None:
        store_id_str: str = typer.prompt("Enter the store_id")
        try:
            store_id = UUID(store_id_str)
        except ValueError:
            typer.echo("Invalid UUID format, please try again.")
    products: List[Product] = []

    # Request the first product ID and quantity
    product_id = typer.prompt("Enter product id")
    quantity = int(typer.prompt(f"Enter quantity for product {product_id}"))
    products.append({"product_id": product_id, "quantity": quantity})

    # For the second and next products, give the option to quit
    while True:
        product_id = typer.prompt("Enter next product id (or 'c' to complete order)")
        if product_id.lower() == "c":
            break
        quantity = int(typer.prompt(f"Enter quantity for product {product_id}"))
        products.append({"product_id": product_id, "quantity": quantity})

    # If no products are added, print error message and exit
    if not products:
        typer.echo("You must order at least one product!")
        return

    # Let's assume your FastAPI server is running locally on port 8000
    fastapi_url = os.getenv("FASTAPI_URL", ngrok_url)

    order_params = {"products": products, "store_id": store_id_str}

    # Send request to create new order
    request_url = f"{fastapi_url}/v1/buyer/orders"
    response = requests.post(request_url, json=order_params, headers=headers)

    if response.status_code == 201:
        typer.echo("Order created successfully!")
    else:
        typer.echo(response.status_code)
        try:
            typer.echo(response.json())
        except JSONDecodeError:
            typer.echo(response)
        typer.echo(
            "Something went wrong. It was reported to the devs. Slack us if you need help."
        )


if __name__ == "__main__":
    app()


# id: cba16cf7-ac5d-477f-8d09-828552ea0b14
# name: 45322386931994
