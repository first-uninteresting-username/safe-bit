{ pkgs, ... }:

{
  languages.python = {
    enable = true;
    venv = {
      enable = true;
      requirements = ''
        -e .
        ruff
        pytest
      '';
    };
  };

  git-hooks.hooks.ruff.enable = true;
}
