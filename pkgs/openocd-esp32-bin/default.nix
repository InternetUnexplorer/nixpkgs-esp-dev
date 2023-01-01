{ stdenv, lib, fetchurl, autoPatchelfHook, zlib, libusb1 }:

let
  sources = builtins.fromJSON (builtins.readFile ./sources.json);
in
stdenv.mkDerivation {
  pname = "openocd-esp32-bin";

  inherit (sources) version;

  src = fetchurl { inherit (sources.artifacts.${stdenv.system}) url hash; };

  nativeBuildInputs = lib.optional (!stdenv.isDarwin) autoPatchelfHook;
  buildInputs = lib.optionals (!stdenv.isDarwin) [ zlib libusb1 ];

  meta = with lib; {
    description = "OpenOCD branch with ESP32 JTAG support";
    homepage = "https://github.com/espressif/openocd-esp32";
    license = licenses.gpl2Plus;
    platforms = lib.attrNames sources.artifacts;
  };
}
