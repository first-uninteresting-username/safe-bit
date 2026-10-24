{ pkgs, ... }:

{
  packages = with pkgs;[
    prettier
  ];

  languages.python = {
    enable = true;
    venv = {
      enable = true;
      requirements = ''
        -e .
        cryptography
        ruff
        pytest
        fastapi[standard]
      '';
    };
  };

  git-hooks.hooks = {
    ruff.enable = true;
    ruff-format.enable = true;
    pyright.enable = true;
    prettier.enable = true;
  };

  scripts = {
    "silence-ruff".exec = "ruff check --fix . && ruff format .";
    "dev-bash".exec = ''
      DB_PATH="$PWD/dev.sqlite3" uvicorn safe_bit.api:app --reload
    '';
    "dev-nushell".exec = ''
      nu -c 'with-env { DB_PATH: $"($env.PWD)/dev.sqlite3" } {
          uvicorn safe_bit.api:app --reload
      }'
    '';
  };
}
