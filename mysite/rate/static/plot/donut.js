/*
 * Play with this code and it'll update in the panel opposite.
 *
 * Why not try some of the options above?
 */
$(function () {
    window.m = Morris.Donut({
        element: 'donut-example',
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
    $(window).on("resize", function(){
      m.redraw();
   });
});
