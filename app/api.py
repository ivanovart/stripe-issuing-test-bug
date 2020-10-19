from typing import Any, Callable, Dict

import stripe
import stripe.error
from fastapi import APIRouter, Depends, Header
from starlette.requests import Request
from stripe.stripe_object import StripeObject

from app.config import settings
from app.errors import StripeBadRequest

router = APIRouter()


def issuing_authorization_request(event: StripeObject):
    stripe_auth = event.data.object
    amount = stripe_auth.pending_request.amount
    decision = amount >= 1000
    [stripe_auth.decline, stripe_auth.approve][decision](
        metadata={"this": "is", "metadata": "to", "save": "!"}
    )


async def get_stripe_event(
    request: Request, stripe_signature: str = Header(..., alias="Stripe-Signature")
):
    try:
        body = await request.body()
        return stripe.Webhook.construct_event(
            payload=body,
            sig_header=stripe_signature,
            secret=settings.STRIPE_WEBHOOK_SECRET,
        )
    except ValueError:
        raise StripeBadRequest("Invalid payload.")
    except stripe.error.SignatureVerificationError:
        raise StripeBadRequest("Invalid signature.")


event_router: Dict[str, Callable[[StripeObject], Any]] = {
    "issuing_authorization.request": issuing_authorization_request,
    "issuing_authorization.created": lambda e: 0,
    "issuing_authorization.updated": lambda e: 0,
    "issuing_card.created": lambda e: 0,
    "issuing_card.updated": lambda e: 0,
    "issuing_cardholder.created": lambda e: 0,
    "issuing_cardholder.updated": lambda e: 0,
    "issuing_dispute.closed": lambda e: 0,
    "issuing_dispute.created": lambda e: 0,
    "issuing_dispute.funds_reinstated": lambda e: 0,
    "issuing_dispute.submitted": lambda e: 0,
    "issuing_dispute.updated": lambda e: 0,
    "issuing_transaction.created": lambda e: 0,
    "issuing_transaction.updated": lambda e: 0,
}


@router.post("/stripe")
def stripe_webhook(
    *, event: StripeObject = Depends(get_stripe_event),
):
    try:
        event_router[event.type](event)
    except KeyError:
        raise StripeBadRequest(f"Can't process event '{event.type}' (#{event.id})")
