Gnome Setup
=========

# TODO add links to tools
This Roles builds a customized gnome desktop environment.
It includes a bunch of [dconf](https://wiki.gnome.org/Projects/dconf) settings as well as extensions and themes beeing installed all in one go.

Extensions (not available on every distro):
- [drive-menu](https://extensions.gnome.org/extension/7/removable-drive-menu/)
- [user-theme](https://extensions.gnome.org/extension/19/user-themes/)
- [appindicator](https://extensions.gnome.org/extension/615/appindicator-support/)
- [sound-output-device-chooser](https://extensions.gnome.org/extension/906/sound-output-device-chooser/)
- no-overview
- tiling-assistant
- dash-to-panel
- system-monitor
- clipboard-indicator

Themes:
- Shell Theme: Lavanda-Dark
- Icon Theme: Tela-circle-purple-dark
- Cursor Theme: Qogir-cursors
- Wallpaper: Dynamic_Wallpapers

The rolse is 

Additionally this role includes a full vagrant based molecule testing setup for CentOSStream9, Almalinux9, Rocky9, Debian12 and Ubuntu22.10 VMs at `extensions/molecule/gnome_setup_test`

Structure
---------
```
📦gnome_setup
 ┣ 📂defaults
 ┃ ┗ 📂main
 ┃ ┃ ┣ 📜common.yml
 ┃ ┃ ┣ 📜extensions.yml
 ┃ ┃ ┗ 📜themes.yml
 ┣ 📂handlers
 ┃ ┗ 📜main.yml
 ┣ 📂meta
 ┃ ┗ 📜main.yml
 ┣ 📂tasks
 ┃ ┣ 📜absent.yml
 ┃ ┣ 📜main.yml
 ┃ ┣ 📜present.yml
 ┃ ┣ 📜present_base_config.yml
 ┃ ┣ 📜present_base_setup.yml
 ┃ ┣ 📜present_extension_handling.yml
 ┃ ┣ 📜present_extensions.yml
 ┃ ┣ 📜present_profile_picture.yml
 ┃ ┣ 📜present_requirements.yml
 ┃ ┣ 📜present_theme_handling.yml
 ┃ ┗ 📜present_themes.yml
 ┣ 📂templates
 ┃ ┗ 📜gnome_profile.j2
 ┣ 📂vars
 ┃ ┗ 📜main.yml
 ┗ 📜README.md
```

The variables are split up into three files according to their content (`common.yml`, `extensions.yml`, `themes.yml`).
The same goes for tasks and they are addtionally prefixed with `present` or `absent` depending on them beeing intended to setup a certain feature or remove it.
As you can see currently the absent implementation only exist in one single file since it's feasable for my curernt usecase.
The tasks related to extensions and tehemes are split up into handelers and the actual setup tasks.
The handlers are meant to take care o preparation steps and check if the extensions/themes are already present or not.
In case not they loop over the tasks to setup and run their install routine implemented in (`present_extension` and `present_themes`)

Requirements
------------

Currently the role expects vagrant users profile pictures to be located at `~/Documents/vagrant` by default, but this will change in future development.
The following packages are required but will also be installed by the role automatically.

**RedHat based systems**
- python3-psutil
- git
- glibc-langpack-en

**Debian based systems**
- python3-psutil
- git

Role Variables
--------------

- defaults/main/common.yml
  - user_install_dir: Custom install directory inside users home directory
  - additional_rhel_repos: Extra repositories for RedHat based distros like CentOSStream9, AlmaLinux, Rocky, ...
  - gnome_packages: Gnome default package lists per distrobution
  - obsolete_packages: Gnome default packages to remove from base install
  - gdm_config_file: Path to gdm configuration file per distribution
  - gnome_base_settings: Gnome dconf settings to change per gnome major version number
- defaults/main/extensions.yml
  - gnome_extensions: list of extensions including their os family specific names and including dconf settings if required
  - git_ext: List of extensions to be installed from custom sources using git and their respective git realted information
  - extension_paths: directories gnome extensions should be installed in
  - obsolete_gnome_extensions: List of extensions to remove from default gnome-shell install
- defaults/main/themes.yml
  - gnome_themes: Dictionary of theme types having the names as their values and dconf dictionary
  - theme_repo: Dictionary of theme names including their git specific information
  - theme_paths: directories gnome themes should be installed in
  - picture_src_path: profile picture source path
  - picture_dest_path: profile picture destination path
  - profile_config_path: Gnome user profile config path
  - profile_pictures: Dictionary of usernames mapped to theit according profile pictures
  - valid_shells: Shell names to grab valid shell user names from

Dependencies
------------

This role doesn't depend on any additional ansible-galaxy roles

Example Playbook
----------------

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:
```yaml
---

- name: Create and configure gnome desktop
  hosts: client
  tasks:
    - name: Include gnome role present
      ansible.builtin.include_role:
        name: gnome_setup
      vars:
        gnome_setup_state: present

...
```
License
-------

MIT
