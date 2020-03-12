// var gulp = require('gulp');

let gulp = require('gulp');
let cleanCSS = require('gulp-clean-css');
let concat = require('gulp-concat');
let csso = require('gulp-csso');
var gulpDebug = require('gulp-debug');
var gzip = require('gulp-gzip');
var rename = require('gulp-rename');

var root_path = "./";
var dest_path = "../www_mini/";
var esp_path = "../www_esp/";
var empty_path = root_path+"empty/";


gulp.task('owl_css', function() {

    gulp.src([root_path + 'lib/bootstrap/*.css', root_path + 'app.css'])
        .pipe(csso())
        .pipe(cleanCSS())
        .pipe(gulpDebug())
        .pipe(concat('app.css'))
        .pipe(gulp.dest(dest_path));
});


gulp.task('owl_gzip', function() {

    gulp.src([dest_path + 'app.js'])
        .pipe(gulpDebug())
        .pipe(gzip())
        .pipe(gulp.dest(dest_path));

    gulp.src([dest_path + 'app.css'])
        .pipe(gulpDebug())
        .pipe(gzip())
        .pipe(gulp.dest(dest_path));

    gulp.src([dest_path + 'favicon.ico'])
        .pipe(gulpDebug())
        .pipe(gzip())
        .pipe(gulp.dest(dest_path));

    gulp.src([dest_path + 'index.html'])
        .pipe(gulpDebug())
        .pipe(gzip())
        .pipe(gulp.dest(dest_path));


    gulp.src([dest_path + 'lib/owl.js'])
        .pipe(gulpDebug())
        .pipe(gzip())
        .pipe(gulp.dest(dest_path+'lib'));

    gulp.src([dest_path + 'lib/css.js'])
        .pipe(gulpDebug())
        .pipe(gzip())
        .pipe(gulp.dest(dest_path+'lib'));

    gulp.src([dest_path + 'xml/app.xml'])
        .pipe(gulpDebug())
        .pipe(gzip())
        .pipe(gulp.dest(dest_path+'xml'));
});



gulp.task('owl_esp', function() {

    //css.js
    gulp.src([dest_path+'lib/css.js.gz'])
        .pipe(gulpDebug())
        .pipe(gulp.dest(esp_path+'lib'));

    gulp.src([empty_path+'empty.js'])
        .pipe(gulpDebug())
        .pipe(rename('css.js'))
        .pipe(gulp.dest(esp_path+'lib'));

    //owl.js
    gulp.src([dest_path+'lib/owl.js.gz'])
        .pipe(gulpDebug())
        .pipe(gulp.dest(esp_path+'lib'));

    gulp.src([empty_path+'empty.js'])
        .pipe(gulpDebug())
        .pipe(rename('owl.js'))
        .pipe(gulp.dest(esp_path+'lib'));

    //XML
    gulp.src([dest_path+'xml/app.xml.gz'])
        .pipe(gulpDebug())
        .pipe(gulp.dest(esp_path+'xml'));

    gulp.src([empty_path+'empty.xml'])
        .pipe(gulpDebug())
        .pipe(rename('app.xml'))
        .pipe(gulp.dest(esp_path+'xml'));


    //app.css
    gulp.src([dest_path+'app.css.gz'])
        .pipe(gulpDebug())
        .pipe(gulp.dest(esp_path));

    gulp.src([empty_path+'empty.css'])
        .pipe(gulpDebug())
        .pipe(rename('app.css'))
        .pipe(gulp.dest(esp_path));

    //app.js
    gulp.src([dest_path+'app.js.gz'])
        .pipe(gulpDebug())
        .pipe(gulp.dest(esp_path));

    gulp.src([empty_path+'empty.js'])
        .pipe(gulpDebug())
        .pipe(rename('app.js'))
        .pipe(gulp.dest(esp_path));

    //favicon.ico
    gulp.src([dest_path+'favicon.ico.gz'])
        .pipe(gulpDebug())
        .pipe(gulp.dest(esp_path));

    gulp.src([empty_path+'empty.ico'])
        .pipe(gulpDebug())
        .pipe(rename('favicon.ico'))
        .pipe(gulp.dest(esp_path));

    //favicon.html
    gulp.src([dest_path+'index.html.gz'])
        .pipe(gulpDebug())
        .pipe(gulp.dest(esp_path));

    gulp.src([empty_path+'empty.html'])
        .pipe(gulpDebug())
        .pipe(rename('index.html'))
        .pipe(gulp.dest(esp_path));

  });

