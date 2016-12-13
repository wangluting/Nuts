jQuery(document).ready(function ($) {
    url = window.location.href;
    desc = 'Hoping you can join with me: '
  $('.rrssb-buttons').rrssb({
    // required:
    title: 'Would you show interest in this plan?',
    url: url,

    // optional:
    description: desc,
    emailBody:  desc + url,
  });
});


