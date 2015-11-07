var Blinky = require('./blinky.js')
var tinycolor = require('tinycolor2');

var LEDS = 60;
var leds = [];
for(var i = 0; i < 60; i++) {
    leds[i] = i;
}

var currentState = {
    enabled: false,
    frame: leds.map(function(led) {
        return {r: (LEDS-led)*4, g: led*4, b: 0};
    })
};

var blinky = new Blinky('/dev/cu.usbmodem1421');

function sendFrame(frame) {
    console.log('Sending frame.');
    frame.forEach(function(color, i) {
        blinky.setPixel(i, color.r, color.g, color.b);
    });
    blinky.show();
}

function solidColor(r, g, b) {
    for(var i = 0; i < 60; i++) {
        blinky.setPixel(i, r, g, b);
    }
    blinky.show();
}

function off() {
    solidColor(0, 0, 0);
}

blinky.on('ready', function() {
    setInterval(function() {
        sendFrame(currentState.frame);
    }, 1000);
});

console.log('Opening connection to AWS IoT.');
var iot = require('aws-iot-device-sdk');
var thingName = 'PipelineLight';
var certDir = '/Users/jwwalker/awscerts/' + thingName;
var config = {
   keyPath: certDir + '/private.pem.key',
  certPath: certDir + '/certificate.pem.crt',
    caPath: certDir + '/verisign-CA.crt',
  clientId: 'BlinkyPi',
    region: 'us-west-2'
};

var shadow = iot.thingShadow(config);

function updateState() {
    console.log('Updating state!');
    var stateUpdate = {
        state: {
            reported: {
                enabled: currentState.enabled,
                frame: currentState.frame.map(function(c) {
                    return tinycolor(c).toHexString();
                })
            }
        }
    }

    shadow.update(thingName, stateUpdate);
}

function applyDelta(delta) {
    state = delta.state
    if('frame' in state) {
        console.log('Applying new frame!');
        currentState.frame = state.frame.map(function(c) {
            return tinycolor(c).toRgb();
        })
    }
};

shadow.on('connect',
    function() {
        console.log('AWS IoT connection opened.');
        //
        // After connecting to the AWS IoT platform, register interest in the
        // Thing Shadow named 'RGBLedLamp'.
        //
        shadow.register(thingName);

        // Update state of the shadow to device's current state.
        setInterval(updateState, 5000);
    });

shadow.on('status',
    function(thingName, stat, clientToken, stateObject) {
       console.log('received '+stat+' on '+thingName+': '+
                   JSON.stringify(stateObject));
    });

shadow.on('delta',
    function(thingName, stateObject) {
        console.log('delta ' + JSON.stringify(stateObject));
        applyDelta(stateObject);
    });

shadow.on('timeout',
    function(thingName, clientToken) {
       console.log('received timeout '+' on '+operation+': '+
                   clientToken);
    });