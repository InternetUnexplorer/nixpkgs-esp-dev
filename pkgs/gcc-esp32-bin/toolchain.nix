{ pname
, version
, sources
, stdenv
, lib
, fetchurl
, autoPatchelfHook
, gcc
, zlib
, python
}:

stdenv.mkDerivation {
  inherit pname version;

  src = fetchurl { inherit (sources.${stdenv.system}) url hash; };

  nativeBuildInputs = lib.optional (!stdenv.isDarwin) autoPatchelfHook;
  buildInputs = lib.optionals (!stdenv.isDarwin) [ gcc.cc.lib zlib python ];

  installPhase = ''
    runHook preInstall
    mkdir $out && cp -r * $out
    runHook postInstall
  '';

  meta = with lib; {
    description = "ESP32* compiler toolchain";
    homepage = "https://github.com/espressif/crosstool-NG";
    license = licenses.gpl3;
    platforms = lib.attrNames sources;
  };
}
