// rollup.config.js
export default {
    // core input options
    input: './index.js',     // required
    // external,
    // plugins,
  
    // advanced input options
    // onwarn,
  
    // danger zone
    // acorn,
    // context,
    // moduleContext,
    // legacy,
  
    output: {  // required (can be an array, for multiple outputs)
      // core output options
      file: '../../../static/js/accessible_text_color.js',    // required
      format: 'iife',  // required
      name: 'accessible_text_color.js',
    //   globals,
  
      // advanced output options
    //   paths,
    //   banner,
    //   footer,
    //   intro,
    //   outro,
    //   sourcemap,
    //   sourcemapFile,
    //   interop,
  
      // danger zone
    //   exports,
    //   amd,
    //   indent
    //   strict
    },
  };