function submitColors(event) {
    event.preventDefault();
    let bgColor = $('#bg-color').val();
    
    $('#aa-colors').html('');
    $('#aaa-colors').html('');

    $.ajax({
        type: "post",
        url: "/api/bg-color",
        data: {
            color: bgColor
        }, 
        dataType: "json",
        success: buildColorList,
    });
}

function buildColorList({background_color: bgColor, aa_colors: A2Colors, aaa_colors: A3Colors}) {
    console.log(bgColor, A2Colors, A3Colors);

    let target = $('input[name=target-standards]:checked').val();;
    
    if (target === 'aa') {
        $(`#${target}-colors`).append(`<h2>WCAG 2.0 Level ${target.toUpperCase()} Color Combinations <br>${A2Colors.length} Colors</h2>`)
        A2Colors.forEach(resultsTemplate(bgColor, target));
    } else if (target === 'aaa') {
        $(`#${target}-colors`).append(`<h2>WCAG 2.0 Level ${target.toUpperCase()} Color Combinations <br>${A3Colors.length} Colors</h2>`)
        A3Colors.forEach(resultsTemplate(bgColor, target));
    }
        
}

function resultsTemplate(bgColor, target) {
    return (color) => {
        $(`#${target}-colors`).append(`<div class="row color-sample"><div class="col-4"><p>Background Color: ${bgColor} </p><p>Text Color: ${color}</p></div><div class="col-8" style="background-color: ${bgColor};"><p style="color: ${color};">The quick brown fox jumps over the lazy dog.</p></div></div>`);
    }
}

$('#bg-color-form').on('submit', submitColors);