# TracRPC
Trac RPC package for Sublime Text 3

Sublime Text Trac-Plugin to interface with an existing trac project.

## Installation

Since this package is still in development, package control is not available as of yet. To install this dev-preview, follow these steps:

- Clone the git repository into your Sublime Text Package directory as a whole
```
git clone https://github.com/lyrixderaven/TracRPC.git
```
- Edit your project settings file to include the settings for your trac instance
```
"settings":
	{
		    "trac_user": "me@myhost.com",
        "trac_pw": "my_super_secret_pw",
        "trac_url": "https://myhost.com/mytrac",
	}
```

Sublime Text should automatically update and include the package; you can check the presence of the package by looking at the settings, which should contain a new entry for TracRPC at `Preferences>Package Settings>TracRPC`

## Usage

Currently, only two commands are implemented:

1. List my tickets (⌘+t, ⌘+t)
2. Insert `[refs #1]` references statement for commit messages (⌘+t,⌘+r)
