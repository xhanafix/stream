{ pkgs }: {
  deps = [
    pkgs.python3
    pkgs.python310Packages.flask
    pkgs.python310Packages.flask-cors
    pkgs.python310Packages.gunicorn
  ];
} 