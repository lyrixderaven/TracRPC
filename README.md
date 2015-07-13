# TracRPC
Trac RPC package for [Sublime Text 3](https://www.sublimetext.com/3)

Sublime Text Trac-Plugin to interface with an existing [trac](http://trac.edgewall.org/) project.

## Preconditions

Besides using the Sublime Text 3 editor, you will need to install the [Trac XML-RPC](https://trac-hacks.org/wiki/XmlRpcPlugin) plugin to your trac instance. Installation instructions can be found on the plugins website. Furthermore, the user you are using to connect to Trac might need to have the `XML_RPC` permission.

## Installation

### Package Control

Since this package has officially been accepted, it is available via [Package Control](https://packagecontrol.io/).

### Manual Installation

For bleeding-edge dev-versions, you can directly clone this github repository. To install this dev-preview, follow these steps:

- Clone the git repository into your Sublime Text Package directory as a whole
```
git clone https://github.com/lyrixderaven/TracRPC.git
```

## Settings

The package requires some settings to work, specifically setting url and authentication credentials for your Trac Environment:

- Edit your project settings file to include the settings for your trac instance
```
"settings":
	{
        "trac_user": "me@myhost.com",
        "trac_pw": "my_super_secret_pw",
        "trac_url": "https://myhost.com/mytrac",
	}
```
Mind that the URL to your trac instance does not need a trailing slash or the `/rpc` postfix; the plugin takes care of that by itself. 

Sublime Text should automatically update and include the package; you can check the presence of the package by looking at the settings, which should contain a new entry for TracRPC at `Preferences>Package Settings>TracRPC`

## Usage

Currently, the following commands are implemented:

1. List my tickets (owned) (⌘+t, ⌘+t)
2. List all my tickets (owned, reported, cc) ((⌘+t, ⌘+a)
3. Insert `[refs #1]` references statement for commit messages (⌘+t, ⌘+r)
4. Add comment to ticket (⌘+t, ⌘+y)
