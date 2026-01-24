{ pkgs }: {
  deps = [
    pkgs.python311
    pkgs.python311Packages.pip
    pkgs.postgresql
  ];
  
  env = {
    PYTHONPATH = "/home/runner/${REPL_SLUG}/backend/src";
  };
}
