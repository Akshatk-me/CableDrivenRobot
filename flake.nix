{
  description = "Course simulator running environment";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs =
    { self, nixpkgs }:
    let
      system = "x86_64-linux";
      pkgs = import nixpkgs { inherit system; };
    in
    {
      devShells.${system}.default = pkgs.mkShell {
        packages = with pkgs; [
          uv
          python311
        ];

        shellHook = ''
                    export LD_LIBRARY_PATH=${
                      pkgs.lib.makeLibraryPath (
                        with pkgs;
                        [
                          stdenv.cc.cc.lib
                          zlib
                          glib
                          libGL
                          libxkbcommon
                          libX11
                          libXext
                          libXrender
                          libXcursor # Fixes the VTK Xcursor warning
                          libXi # Common VTK dependency for mouse input
                          libXrandr # Common VTK dependency for window resizing
                          xcbutilcursor # Fixes the Qt 6.5 xcb cursor error
                          # The Full X11 / XCB Suite for Qt & VTK ---
                          libX11
                          libXext
                          libXrender
                          libXcursor
                          libXi
                          libXrandr
                          libxcb
                          xcbutil
                          xcbutilwm
                          xcbutilimage
                          xcbutilkeysyms
                          xcbutilrenderutil
                          fontconfig.lib
                          freetype
                          dbus
                          wayland
                        ]
                      )
                    }:$LD_LIBRARY_PATH

                    # Ignore global NixOS Qt theming for this PyPI-based app
                    unset QT_STYLE_OVERRIDE
                    unset QT_QPA_PLATFORMTHEME
          	  

                    # Force Qt to use X11 (Xwayland) because VTK cannot handle Wayland windows natively
                    export QT_QPA_PLATFORM=xcb

                    echo "General Dev Shell Loaded!"
        '';

      };
    };
}
