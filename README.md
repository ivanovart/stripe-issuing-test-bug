# Stripe issuing test bug

This small project is here to demonstrate a bug on stripe platform in test mode.
It is a single route HTTP server written using Fast-API and Stripe SDK.

# How to run
1. Cp `template.env` file to `.env`
1. Put your configs to `.env` (wh secret and stripe api key)
1. To run installing all required packages locally execute: `pipenv install` and `pipenv run uvicorn app.main:app`
1. To run using docker execute `docker build -t stripe-bug .` and `docker run -p "8000:8000" --env-file=.env --rm stripe-bug`
1. Subscribe to webhook using CLI `stripe listen --forward-to=http://localhost:8000/stripe --events issuing_authorization.request`

# How to reproduce
After you started server and configured webhook you can:
1. Trigger event using CLI (`stripe trigger issuing_authorization.request`) => the metadata will be erased
1. Trigger event using Dashboard ([select a create an issued card](https://dashboard.stripe.com/test/issuing/overview), then click "Create test authorisation") => the metadata will be erased
1. Create a new [payment](https://dashboard.stripe.com/test/payments/new) using issued card details => 🎉

To have authorization accepted use an amount >= 10$
