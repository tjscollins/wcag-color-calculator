const color = require('color-convert');

class ColorValue {
    constructor(hexColor) {
        this._rgb = color.hex.rgb(hexColor);
        this._hex = hexColor;
    }

    hex() {
        return color.rgb.hex(this._rgb);
    }

    css() {
        return color.rgb.keyword(this._rgb);
    }

    rgb() {
        return this._rgb;
    }

    hsl() {
        return color.rgb.hsl(this._rgb);
    }
}

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
                background_color: new ColorValue(background_color),
                aa_colors: aa_colors.map((color) => new ColorValue(color)),
                aaa_colors: aaa_colors.map((color) => new ColorValue(color)),
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
        $(`#${target}-colors`).append(`<div class="row color-sample border border-bottom-0 border-dark"><div class="col-12 text-center" style="background-color: #${bgColor.hex()};"><p style="color: #${tColor.hex()};">The quick brown fox jumps over the lazy dog.</p></div><div class="col-12 d-flex flex-row justify-content-around" style="background-color: #${bgColor.hex()}; color: #${tColor.hex()};"><p>Background Color: ${bgColor.hex()} </p><p>Text Color: ${tColor.hex()} </p><p>Closest Name: ${tColor.css()}</div></div>`);
    }
}

function filterColors({
    currentTarget,
    currentTarget: {
        value
    },
    ...event
}) {
    let {
        background_color: {_hex},
        aa_colors,
        aaa_colors
    } = JSON.parse(localStorage.getItem('data'));
    aa_colors = aa_colors.map(({_hex}) => new ColorValue(_hex))
        .filter(color => {
            return color.hsl()[0] === parseInt(value) || value === 'all';
        });
    aaa_colors = aaa_colors.map(({_hex}) => new ColorValue(_hex))
    .filter(color => {
        return color.hsl()[0] === parseInt(value) || value === 'all';
    });
    buildColorList({
        background_color: new ColorValue(_hex),
        aa_colors,
        aaa_colors
    });
}

localStorage.clear();
$('#bg-color-form').on('submit', submitColors);
$('input[type="radio"][name="hue-chooser"]').on('change', filterColors);