    //------------------------------------------------------------------------------
    // Responsive plugin
    //------------------------------------------------------------------------------
    export function ResponsivePlugin(env) {
      const isMobile = () => window.innerWidth <= 768;
      env.isMobile = isMobile();
      const updateEnv = owl.utils.debounce(() => {
          if (env.isMobile !== isMobile()) {
              env.isMobile = !env.isMobile;
              env.qweb.forceUpdate();
          }
      }, 15);
      window.addEventListener("resize", updateEnv);
    }
