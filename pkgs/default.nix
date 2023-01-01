pkgs@{ callPackage, ... }:

(import ./gcc-esp32-bin pkgs) // {
  # esp-idf = callPackage ./esp-idf { };
  openocd-esp32-bin = callPackage ./openocd-esp32-bin { };
}
