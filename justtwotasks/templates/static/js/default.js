// Hide the done button
$("#task-form-submit").hide();

// Submit form on onfocus of an input
$(".task-input").focusout(function() {
    $("form#task-form").submit();
});
