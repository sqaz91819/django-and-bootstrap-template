$(function() {

    Morris.Area({
        element: 'morris-area-chart',
        data: [{
            period: '2010 Q1',
            iphone: date_info[5][2]
            /*
            ipad: null,
            itouch: 0
            */
        }, {
            period: '2010 Q2',
            iphone: date_info[4][2],
            ipad: 0,
            itouch: 0
        }, {
            period: '2010 Q3',
            iphone: date_info[3][2],
            ipad: 0,
            itouch: 0
        }, {
            period: '2010 Q4',
            iphone: date_info[2][2],
            ipad: 0,
            itouch: 0
        }, {
            period: '2011 Q1',
            iphone: date_info[1][2],
            ipad: 0,
            itouch: 0
        }, {
            period: '2011 Q2',
            iphone: date_info[0][2],
            ipad: 0,
            itouch: 0
        }, {
            period: '2011 Q3',
            iphone: 0,
            ipad: 0,
            itouch: 0
        }, {
            period: '2011 Q4',
            iphone: 0,
            ipad: 0,
            itouch: 0
        }, {
            period: '2012 Q1',
            iphone: 0,
            ipad: 0,
            itouch: 0
        }, {
            period: '2012 Q2',
            iphone: 0,
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
