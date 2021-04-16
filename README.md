# WM Theme Changer

Within my preferred window manager, I've enjoyed using pywal to generate and apply color schemes, but find myself manually tweaking the values and running additional configuration commands to use the color scheme (for example, updating scheming for spicetify or zathura). As a way of managing and applying these color schemes, I wrote a quick wrapper that eases some of this, and allows for storage of favorite color schemes, application of a specific or random color scheme, and provides script hooks to apply any additional config one may require.

## Basic Usage
```
usage: Theme Changer [-h] (-s SAVE_THEME | -a APPLY_THEME | -f APPLY_THEME_FILE | -r | -l) [-v]

optional arguments:
  -h, --help            show this help message and exit
  -s SAVE_THEME, --save-theme SAVE_THEME
                        Save current theme
  -a APPLY_THEME, --apply-theme APPLY_THEME
                        Apply stored theme by name
  -f APPLY_THEME_FILE, --apply-theme-file APPLY_THEME_FILE
                        Apply stored theme file
  -r, --random-theme    Apply random stored theme
  -l, --list-theme      List all stored themes
  -v, --verbose         Display additional information
```

### Saving a Theme
After generating a theme with `wal -i` and customizing it to your liking, it can be saved with:

* `theme-change -s name`

This will:
* copy the json definition from `~/.cache/wal/colors.json` into the `~/.config/theme-change/themes` directory as "name.json"
* copy the background image file into the `~/.config/theme-change/backgrounds` directory
* update the "wallpaper" key in "name.json" accordingly

### Applying a Theme
Saved themes can be applied in several ways:
* `theme-change -a name` will apply the theme with name "name"
* `theme-change -f file` will apply a specific theme file
* `theme-change -r` will apply a random theme from `~/.config/theme-change/themes`


## Script Hooks
After successful application of a theme, all .sh scripts in `~/.config/theme-change/scripts` will be run. This allows for additional application theming to be applied with the newly-applied color scheme.


For example, if you wanted to force spicetify (spotify theming) to update after a theme change, you could add this script:
```
==> ~/.config/theme-change/scripts/spicetify.sh <==
#!/bin/bash
spicetify apply -q
```

Additionally, these scripts are run with a single argument, $1, which holds the full path to the json theme definition, allowing your script to consume those values. For example, you could use openrgb to update the color of your keyboard's backlight based on a generated color:
```
==> ~/.config/theme-change/scripts/openrgb.sh <==
#!/bin/bash
# This will be called with a single argument, $1, which points at the full path of the applied theme

openrgb -c $(awk -F'[\"#]' '/color4/{print $(NF-1)}' $1)
```

These will usually execute silently- pass `-v` to outline which scripts are running and see their stdout/stderr for troubleshooting.