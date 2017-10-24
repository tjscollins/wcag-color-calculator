const color = require('color-convert');

function submitColors(event) {
    event.preventDefault();
    let bgColor = $('#bg-color').val();

    $('#aa-colors').html('');
    $('#aaa-colors').html('');
    $('#hue-all').prop('checked', true);

    $.ajax({
        type: "post",
        url: "/api/bg-color",
        data: {
            color: bgColor
        },
        dataType: "json",
        success: ({
            background_color,
            aa_colors,
            aaa_colors
        }) => {
            let data = {
                background_color,
                aa_colors: [... new Set(aa_colors.map(color.hex.keyword))],
                aaa_colors: [... new Set(aaa_colors.map(color.hex.keyword))]
            }
            localStorage.setItem('data', JSON.stringify(data));
            buildColorList(data);
        },
    });
}

function buildColorList({
    background_color: bgColor,
    aa_colors: A2Colors,
    aaa_colors: A3Colors
}) {
    console.log(bgColor, A2Colors, A3Colors);

    let target = $('input[name=target-standards]:checked').val();
    $(`#${target}-colors`).html('');

    if (target === 'aa') {
        $(`#${target}-colors`).append(`<h2>WCAG 2.0 Level ${target.toUpperCase()} Color Combinations <br>${A2Colors.length} Colors</h2>`)
        A2Colors.forEach(resultsTemplate(bgColor, target));
    } else if (target === 'aaa') {
        $(`#${target}-colors`).append(`<h2>WCAG 2.0 Level ${target.toUpperCase()} Color Combinations <br>${A3Colors.length} Colors</h2>`)
        A3Colors.forEach(resultsTemplate(bgColor, target));
    }

}

function resultsTemplate(bgColor, target) {
    return (tColor) => {
        $(`#${target}-colors`).append(`<div class="row color-sample border border-bottom-0 border-dark"><div class="col-12 text-center" style="background-color: ${bgColor};"><p style="color: ${tColor};">The quick brown fox jumps over the lazy dog.</p></div><div class="col-12 d-flex flex-row justify-content-around" style="background-color: ${bgColor}; color: ${tColor};"><p>Background Color: ${color.hex.keyword(bgColor)} </p><p>Text Color: ${tColor}</p></div></div>`);
    }
}

function filterColors({
    currentTarget,
    currentTarget: {
        value
    },
    ...event
}) {
    let selectedColor = color.hsl.rgb(parseInt(value), 100, 50);
    let {
        background_color,
        aa_colors,
        aaa_colors
    } = JSON.parse(localStorage.getItem('data'));
    aa_colors = aa_colors.filter((kColor) => {
        return color.keyword.hsl(kColor)[0] === parseInt(value) || value === 'all';
    });
    aaa_colors = aaa_colors.filter((kColor) => {
        return color.keyword.hsl(kColor)[0] === parseInt(value) || value === 'all';
    });
    buildColorList({
        background_color,
        aa_colors,
        aaa_colors
    });
}

localStorage.clear();
$('#bg-color-form').on('submit', submitColors);
$('input[type="radio"][name="hue-chooser"]').on('change', filterColors);