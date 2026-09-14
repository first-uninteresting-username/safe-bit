{ pkgs, ... }:

{
  languages.python = {
    enable = true;
    venv = {
      enable = true;
      requirements = ''
        pytest
        ruff
      '';
    };
  };

  git-hooks.hooks.ruff.enable = true;
}
