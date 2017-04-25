var heatmap
/*
$(window).onload(function(){
    heatmap = h337.create({
        container: document.getElementById('heatmapContainer'),
        // a waterdrop gradient ;-)
        gradient: { .1: 'rgba(0,0,0,0)', 0.25: "rgba(0,0,90, .6)", .6: "blue", .9: "cyan", .95: 'rgba(255,255,255,.4)' },
        maxOpacity: .6,
        radius: 10,
        blur: .90
    });
})
*/
function setup() {
    // width = (+window.getComputedStyle(document.body).width.replace(/px/, ''));
    // height = (+window.getComputedStyle(document.body).height.replace(/px/, ''));
    width = document.getElementById('heat-map').offsetWidth;
    height = document.getElementById('heat-map').offsetHeight;
    console.log("width is: ", width, "height is: ", height);
    heatmap = h337.create({
        container: document.getElementById('canvas'),
        gradient: { .1: "rgba(146, 254, 157, 1)", 0.4: "rgba(0, 201, 255, .5)"},
        maxOpacity: .9,
        radius: 10,
        blur: 0.1
    });


    /*
    console_columns = [];

    for (var column_index = 0; column_index < 64; column_index++) {
        var column = [];
        for (var entry_index = 0; entry_index < 32; entry_index++) {
            column[entry_index] = 0;
        }
        console_columns.push(column);
    }
    */
}

function update_heat_map(msg) {
        var max = 100;
        var min = 0;
        var data = {
            max: 1,
            min: 0,
            data: [
                0
            ]
        };

        var x_serv = (msg.x * width) >> 0;
        var y_serv = (msg.y * height) >> 0;
        console.log("x is ", x_serv, "y is ", y_serv);
        var c = 100;
        var r = (500) >> 0;

        // add the datapoint to heatmap instance
        heatmap.setData(data);
        heatmap.addData({ x: x_serv, y: y_serv, value: c, radius: r });
    /*
    x = msg.x
    y = msg.y

    var fifo_queue = [];
    for (var index = 0; index < 32; index++) {
        fifo_queue[index] = 0;
    }

    for (var syscall in msg) {
        var val = message[syscall];
        for (result_index in val) {
            var lat_start = val[result_index][0][0];
            var count = val[result_index][1];
            fifo_queue[Math.floor(lat_start / 2)] += count;
        }
    }
    consule_columns.shift();
    console_columns.push(syscall_by_latency);
    drawArray(console_columns);
    */
}

/*drawArray(){

}*/

function load_socket() {
    setup();

    var socket = io.connect('http://' + document.domain + ':' + location.port + '/test');
    
    socket.on('Connect', function () {
        console.log('on connection');

    });
    socket.on('newnumber', function (msg) {
        console.log("Received number " + ", " + msg.x + ", " + msg.y);
        update_heat_map(msg)
    });

}
    


/*



    // boundaries for data generation
    var width = (+window.getComputedStyle(document.body).width.replace(/px/, ''));
    var height = (+window.getComputedStyle(document.body).height.replace(/px/, ''));

    var generate = function () {
        var max = 100;
        var min = 0;
        var t = [];

        var x = (Math.random() * width) >> 0;
        var y = (Math.random() * height) >> 0;
        var c = 100;
        var r = (Math.random() * 100) >> 0;

        // add the datapoint to heatmap instance
        heatmap.addData({ x: x, y: y, value: c, radius: r });
    };
    // this generates new datapoints in a kind of random timing
    setTimeout(function test() {
        var rand = (Math.random() * 500) >> 0;
        generate();
        setTimeout(test, rand);
    }, 100);
    //connect to the socket server.
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/test');
    var numbers_received = [];

    //receive details from server
    socket.on('newnumber', function(msg) {
        console.log("Received number " + msg.number + ", " + msg.x + ", " + msg.y);
        //maintain a list of ten numbers
        if (numbers_received.length >= 10){
            numbers_received.shift()
        }            
        numbers_received.push(msg.number);
        numbers_string = '';
        for (var i = 0; i < numbers_received.length; i++){
            numbers_string = numbers_string + '<p>' + numbers_received[i].toString() + '</p>';
        }
        $('#log').html(numbers_string);
    });

});
*/
