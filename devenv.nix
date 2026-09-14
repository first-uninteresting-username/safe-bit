{ pkgs, ... }:

{
  languages.python = {
    enable = true;
    venv = {
      enable = true;
      requirements = ''
        -e .
        ruff
      '';
    };
  };

  git-hooks.hooks.ruff.enable = true;
}
