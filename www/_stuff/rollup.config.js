// import nodeResolve from 'rollup-plugin-node-resolve';
// import typescript from 'rollup-plugin-typescript'
// import esModuleInterop from 'rollup-plugin-es-module-interop'
// import commonjs from 'rollup-plugin-commonjs';
import babel from 'rollup-plugin-babel';
import copy from 'rollup-plugin-copy'


var root_path = "./";
var mini_path = "../www_mini/";

export default [{
    input: ['main.js', ],
    output: [{file: mini_path+'app.js', format: 'cjs' }],
    plugins: [

        babel({
            exclude: 'node_modules/**',
            // presets: ['es2015-rollup', 'stage-0'],     //  <- stage-0 had to be added
            runtimeHelpers: true,
             plugins: ["@babel/plugin-proposal-class-properties"]
        }),
        copy({
          targets: [
              { src: 'lib/owl.js', dest: mini_path+'lib' },
              { src: 'lib/css.js', dest: mini_path+'lib' },
              { src: 'xml/app.xml', dest: mini_path+'xml' },
              { src: 'index_mini.html', dest: mini_path, rename: 'index.html' },
              { src: 'favicon.ico', dest: mini_path },

          ]
        }),
    ],
}];