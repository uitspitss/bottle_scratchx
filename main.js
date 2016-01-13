(function(ext){
  var device = null;

  ext._deviceConnected = function(dev){
    if(device) return;
    device = dev;
    console.log(device);
    device.open();
  };

  ext._deviceRemoved = function(dev){
    if(device != dev) return;
    device = null;
  };

  ext._shutdown = function(){
    if(device) device.close();
    device = null;
  };

  ext._getStatus = function(){
    if(!device) return {status: 1, msg: 'digiUSB disconnected'};
    return {status: 2, msg: 'digiUSB connectd'};
  };

  ext.blink = function(red, green, blue){
    $.ajax({
      type: "GET",
      url: "http://localhost:5000/blink",
      dataType: "script",
      data: {
        red: red,
        green: green,
        blue: blue
      }
    });
  };

  var descriptor = {
    blocks: [
      ["",  "red: %n, green: %n, blue: %n で光らせる", "blink",
       "100", "100", "100"]
    ],
    menus: {},
    url: 'http://localhost:5000'
  };

  var hid_info = {type: 'hid', vendor: 0x16c0, product: 0x05df};
  console.log(ScratchExtensions.register('DigiUSB', descriptor, ext, hid_info));
})({});
