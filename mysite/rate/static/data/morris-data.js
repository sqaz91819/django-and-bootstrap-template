$(function() {

    Morris.Area({
        element: 'morris-area-chart',
        data: [{
            period: date_info[5][0].toString().concat('-', date_info[5][1].toString()),
            iphone: date_info[5][2]
            /*
            ipad: null,
            itouch: 0
            */
        }, {
            period: date_info[4][0].toString().concat('-', date_info[4][1].toString()),
            iphone: date_info[4][2],
            ipad: 0,
            itouch: 0
        }, {
            period: date_info[3][0].toString().concat('-', date_info[3][1].toString()),
            iphone: date_info[3][2],
            ipad: 0,
            itouch: 0
        }, {
            period: date_info[2][0].toString().concat('-', date_info[2][1].toString()),
            iphone: date_info[2][2],
            ipad: 0,
            itouch: 0
        }, {
            period: date_info[1][0].toString().concat('-', date_info[1][1].toString()),
            iphone: date_info[1][2],
            ipad: 0,
            itouch: 0
        }, {
            period: date_info[0][0].toString().concat('-', date_info[0][1].toString()),
            iphone: date_info[0][2],
            ipad: 0,
            itouch: 0
        }],
        xkey: 'period',
        ykeys: ['iphone', 'ipad', 'itouch'],
        labels: ['iPhone', 'iPad', 'iPod Touch'],
        pointSize: 2,
        hideHover: 'auto',
        resize: true
    });

    Morris.Donut({
        element: 'morris-donut-chart',
        data: [
            {label: "Positive Articles", value: pos_num},
            {label: "Neutral Articles", value: neutral_num},
            {label: "Negative Articles", value: neg_num}
        ],
        colors: [
         "green",
         "orange",
         "red"
        ],
        resize: true
    });

    Morris.Bar({
        element: 'morris-bar-chart',
        data: [{
            y: 'Origin',
            a: ori,
            b: 0
        }, {
            y: 'fast',
            a: fast_text,
            b: 0
        }, {
            y: 'LSTM',
            a: 0,
            b: 0
        }, {
            y: '2009',
            a: 0,
            b: 0
        }],
        xkey: 'y',
        ykeys: ['a', 'b'],
        labels: ['Series A', 'Series B'],
        hideHover: 'auto',
        resize: true
    });
    
});
