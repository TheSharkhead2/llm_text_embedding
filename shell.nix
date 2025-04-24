{ pkgs ? import <nixpkgs> { } }:

pkgs.mkShell {
  name = "dev-shell";

  # buildInputs = with pkgs; [ jupyter ];

  packages = [
    (pkgs.python312.withPackages (ps: [
      ps.numpy
      ps.python-lsp-server
      ps.matplotlib
      ps.scikitlearn
      ps.kaggle
    ]))
  ];
}

