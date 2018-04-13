import ssl, os
import json
import paho.mqtt.client as mqtt
import sys

import logging
logger = logging.getLogger(__name__)
# TODO: Remove this from the library
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

things = ['TestThing']

def shadow_topic(thing, suffix):
    return "$aws/things/{}/shadow/{}".format(thing, suffix)

def on_connect(client, userdata, flags, result_code):
    logger.info("Connected with result code: %s", result_code)
    
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
        
    for thing in things:
        topic = shadow_topic(thing, '#')
        client.subscribe(topic)

def on_disconnect(client, userdata, result_code):
    logger.warning("Disconnected with result code: %s", result_code)

def on_message(client, userdata, message):
    logger.debug("Received message from topic '%s': %s", message.topic, message.payload)

def on_subscribe(client, userdata, topic, granted_qos):
    logger.debug("Subscribed to topic '%s' with qos %s.", topic, granted_qos)
    get_state(client, 'TestThing')
    update_state(client, 'TestThing')

log_levels = {
    mqtt.MQTT_LOG_INFO: logging.INFO,
    mqtt.MQTT_LOG_NOTICE: logging.WARNING,
    mqtt.MQTT_LOG_WARNING: logging.WARNING,
    mqtt.MQTT_LOG_ERR: logging.ERROR,
    mqtt.MQTT_LOG_DEBUG: logging.DEBUG
}

def on_log(client, obj, level, msg):
    logger.log(log_levels[level], msg)        

state = {}

def get_state(client, thing_name):
    client.publish(shadow_topic(thing_name, 'get'))

def update_state(client, thing_name):
    message = {
        "state": {
            "reported": state
        }
    }
    
    client.publish(shadow_topic(thing_name, 'update'), json.dumps(message))

def on_update_accepted(client, userdata, message):
    payload = json.loads(message.payload.decode('utf-8'))
    delta = payload['state']
    print("Update accepted {}".format(delta))
    
    state.update(delta)
    print("New state {}".format(state))
    
    update_state(client, 'TestThing')
    
client = mqtt.Client()
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message
client.on_subscribe = on_subscribe
client.on_log = on_log

cert_dir = os.path.expanduser('~/.awscerts/PipelineLight/')
ca_certs = os.path.join(cert_dir, 'verisign-CA.crt')
certfile = os.path.join(cert_dir, 'certificate.pem.crt')
keyfile = os.path.join(cert_dir, 'private.pem.key')
client.tls_set(ca_certs, certfile=certfile, keyfile=keyfile, tls_version=ssl.PROTOCOL_TLSv1_2)

for thing in things:
    client.message_callback_add(shadow_topic(thing, 'update/accepted'), on_update_accepted)

client.connect("data.iot.us-west-2.amazonaws.com", 8883, 60)
client.loop_forever()
