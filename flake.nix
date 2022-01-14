{
  inputs =
    { nixpkgs.url = "github:NixOS/nixpkgs?ref=nixos-21.11";
      nixng.url = "github:MagicRB/NixNG";
    };

  outputs =
    { self, nixpkgs, nixng }:
    let
      supportedSystems = [ "x86_64-linux" ];
      forAllSystems' = nixpkgs.lib.genAttrs;
      forAllSystems = forAllSystems' supportedSystems;
      pkgsForSystems = system: import nixpkgs { inherit system; };
      nglib = nixng.nglib nixpkgs.lib;
    in
      { dockerImages = forAllSystems (system:
          {
            db = nglib.makeSystem
              { inherit nixpkgs;
                system = "x86_64-linux";
                name = "shop-db";
                config =
                  ({ pkgs, ... }:
                    { dumb-init =
                        { enable = true;
                          type.services = { };
                        };
                      services.postgresql =
                        { enable = true;
                          package = pkgs.postgresql_12;

                          ensureDatabases =
                            [ "shop"
                            ];

                          ensureUsers =
                            [ { name = "shop";
                                ensurePermissions =
                                  { "DATABASE \"shop\"" = "ALL PRIVILEGES"; };
                              }
                            ];

                          authentication =
                            ''
                              host all all 0.0.0.0/0 trust
                            '';

                          enableTCPIP = true;
                        };
                    });
              };
          }
        );

        devShell = forAllSystems (system:
          let pkgs = pkgsForSystems system;
          in
            pkgs.mkShell {
              nativeBuildInputs = with pkgs;
                [ postgresql_12
                ];
            }
        );
      };
}
