$(function() {

    Morris.Area({
        element: 'morris-area-chart',
        data: [{
            period: '2010 Q1',
            iphone: 266,
            ipad: null,
            itouch: 264
        }, {
            period: '2010 Q2',
            iphone: 0,
            ipad: 0,
            itouch: 0
        }, {
            period: '2010 Q3',
            iphone: 0,
            ipad: 0,
            itouch: 0
        }, {
            period: '2010 Q4',
            iphone: 376,
            ipad: 359,
            itouch: 568
        }, {
            period: '2011 Q1',
            iphone: 680,
            ipad: 191,
            itouch: 293
        }, {
            period: '2011 Q2',
            iphone: 570,
            ipad: 423,
            itouch: 181
        }, {
            period: '2011 Q3',
            iphone: 420,
            ipad: 375,
            itouch: 188
        }, {
            period: '2011 Q4',
            iphone: 173,
            ipad: 597,
            itouch: 575
        }, {
            period: '2012 Q1',
            iphone: 187,
            ipad: 440,
            itouch: 228
        }, {
            period: '2012 Q2',
            iphone: 432,
            ipad: 513,
            itouch: 791
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
            y: '2006',
            a: 100,
            b: 90
        }, {
            y: '2007',
            a: 75,
            b: 65
        }, {
            y: '2008',
            a: 50,
            b: 40
        }, {
            y: '2009',
            a: 75,
            b: 65
        }, {
            y: '2010',
            a: 50,
            b: 40
        }, {
            y: '2011',
            a: 75,
            b: 65
        }, {
            y: '2012',
            a: 100,
            b: 90
        }],
        xkey: 'y',
        ykeys: ['a', 'b'],
        labels: ['Series A', 'Series B'],
        hideHover: 'auto',
        resize: true
    });
    
});
