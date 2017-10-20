function submitColors(event) {
    event.preventDefault();
    let bgColor = $('#bg-color').val();
    
    $.ajax({
        type: "post",
        url: "/api/bg-color",
        data: {
            color: bgColor
        }, 
        dataType: "json",
        success: function (response) {
            console.log(response)
        },
    });
}

$('#bg-color-form').on('submit', submitColors);