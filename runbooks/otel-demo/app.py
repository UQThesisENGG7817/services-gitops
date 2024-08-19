from flask import Flask
from random import randint

from opentelemetry import trace, metrics
import logging

# Initialize tracer globally
tracer = trace.get_tracer_provider().get_tracer(__name__)

# Initialize metrics globally
meter = metrics.get_meter_provider().get_meter(__name__)
request_counter = meter.create_counter(name="request_counter", description="Number of requests", unit="1")

app = Flask(__name__)

@app.route("/rolldice")
def roll_dice():
    return str(do_roll())

def do_roll():
    res = randint(1, 6)

    with tracer.start_as_current_span("do_roll"):
        current_span = trace.get_current_span()
        current_span.set_attribute("roll.value", res)
        current_span.add_event("This is a span event")

        logging.getLogger().error("Derp! Brisbane, we have a major problem.")
        
        request_counter.add(1)

    return res

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8082, debug=True, use_reloader=False)
