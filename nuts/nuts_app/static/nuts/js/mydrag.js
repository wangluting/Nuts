function update_state(str, id, point) {
    $.post("/nuts/update-state/" + id, {state: str, point: point})
        .done(function(data) {
      });
}

// bw: surprise
function open() {
    TweenLite.to($(this).find('.card'), 0.8, {
        rotationY: -120,
        ease: Back.easeOut
    });
    TweenLite.to('.card__contents', 1.2, {
        scale: 1,
        autoAlpha: 1,
        delay: 0.5,
        ease: Elastic.easeOut
    });

}

$(document).ready(function () {
    //console.log(document.getElementById("TODO"));
    //dragula([document.getElementById("TODO"), document.getElementById("DOING"), document.getElementById("DONE")]);

    dragula([TODO, DOING, DONE]).on('drag', function (el) {
    }).on('drop', function (el) {


        var str = el.parentNode.id;
        var point = 0;

        // give animation if done
        if (str == "DONE") {
            // bw : surprise
            open();
            point = 5;
            var random = Math.random();
            if(random > 0.75) {
            	document.getElementById("card_content").innerHTML = "<p>You are amazing!</p>"
                                + "<p>Congratulation on finishing your plan: </p>"
                                + "<p class='surprise'><b>" + document.getElementById("nutTitle_" + el.id).innerHTML + "</p>" +
                                		"<p>It's your lucky day! You just earned 20 points for finishing " + document.getElementById("nutTitle_" + el.id).innerHTML + " !</p></b>";
            	point = 20;
            }
            else
            	document.getElementById("card_content").innerHTML = "<p>You are amazing!</p>"
                    + "<p>Congratulation on finishing your plan: </p>"
                    + "<p class='surprise'><b>" + document.getElementById("nutTitle_" + el.id).innerHTML + "</p>" +
                    		"<p>You just earned yourself 5 points for finishing " + document.getElementById("nutTitle_" + el.id).innerHTML + " !</p></b>";
        }

        var id = el.id.split("_")[1];
        update_state(str, id, point);
    });

    // bw: surprise
    TweenLite.set('.card-wrapper');
    TweenLite.set('.card', {
        transformStyle: 'preserve-3d',
        transformOrigin: 'left 50%',
        transformPerspective: 1800
    });
    TweenLite.set('.back', { rotationY: 180 });
    TweenLite.set([
        '.back',
        '.front'
    ], { backfaceVisibility: 'hidden' });
    TweenLite.set('.card__contents', {
        scale: 0,
        autoAlpha: 0
    });
    $('.card-wrapper').bind({
        click: function () {
            TweenLite.to($(this).find('.card'), 0.8, {
                rotationY: -120,
                ease: Back.easeOut
            });
            TweenLite.to('.card__contents', 1.2, {
                scale: 1,
                autoAlpha: 1,
                delay: 0.5,
                ease: Elastic.easeOut
            });
        }
    });
    $('.close').bind({
        click: function () {
            TweenLite.to('.card__contents', 0.4, {
                scale: 0,
                autoAlpha: 0,
                ease: Power1.easeOut
            });
            TweenLite.to('.card', 0.6, {
                rotationY: 0,
                delay: 0.5,
                ease: Power1.easeOut
            });
        }
    });
    TweenLite.set('.text-box', {
        autoAlpha: 0,
        y: '20px'
    });

});
