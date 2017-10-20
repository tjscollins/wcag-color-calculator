const gulp = require('gulp');
const livereload = require('gulp-livereload');
const rollup = require('gulp-better-rollup');
const babel = require('rollup-plugin-babel');
const rename = require('gulp-rename');

gulp.task('rollup', () => {
    gulp.src('src/index.js')
    .pipe(rollup({
        plugins: [babel()]
    }, {
        format: 'iife'
    }))
    .pipe(rename({
        basename: 'accessible_text_color'
    }))
    .pipe(gulp.dest('../../../static/js/'))
});

gulp.task('watch', ['rollup'], () => {
    livereload.listen();
    gulp.watch('./src/**/*js', ['rollup'])
});