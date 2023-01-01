{ lib, callPackage, ... }:

let
  sources = builtins.fromJSON (builtins.readFile ./sources.json);
  version = sources.version;
  targets = lib.attrNames sources.artifacts;

  toolchain = target:
    callPackage ./toolchain.nix {
      pname = "gcc-${target}-bin";
      inherit version;
      sources = sources.artifacts.${target};
    };
in
lib.listToAttrs
  (map (pkg: lib.nameValuePair pkg.pname pkg) (map toolchain targets))
