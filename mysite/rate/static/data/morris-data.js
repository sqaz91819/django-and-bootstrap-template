$(function() {

    Morris.Area({
        element: 'morris-area-chart',
        data: [{
            period: date_info[5][0].toString().concat('-', date_info[5][1].toString()),
            iphone: date_info[5][2]
        }, {
            period: date_info[4][0].toString().concat('-', date_info[4][1].toString()),
            iphone: date_info[4][2]
        }, {
            period: date_info[3][0].toString().concat('-', date_info[3][1].toString()),
            iphone: date_info[3][2]
        }, {
            period: date_info[2][0].toString().concat('-', date_info[2][1].toString()),
            iphone: date_info[2][2]
        }, {
            period: date_info[1][0].toString().concat('-', date_info[1][1].toString()),
            iphone: date_info[1][2]
        }, {
            period: date_info[0][0].toString().concat('-', date_info[0][1].toString()),
            iphone: date_info[0][2]
        }],
        xkey: 'period',
        ykeys: ['iphone'],
        labels: ['Total articles'],
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
            old: old_ori,
            new: new_ori,
            total: ori
        }, {
            y: 'FastText',
            old: old_fast_text,
            new: new_fast_text,
            total: fast_text
        }, {
            y: 'CNN-LSTM',
            old: old_cnn_lstm,
            new: new_cnn_lstm,
            total: cnn_lstm
        }, {
            y: 'CNN-2LSTM',
            old: old_cnn_2lstm,
            new: new_cnn_2lstm,
            total: cnn_2lstm
        }],
        xkey: 'y',
        ykeys: ['old', 'new', 'total'],
        labels: ['Score of Known Data', 'Score of Unknown Data', 'Total'],
        hideHover: 'auto',
        resize: true
    });
    
});
