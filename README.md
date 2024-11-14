# Limnoria BlueSky Plugin

A Limnoria plugin that monitors IRC channels for BlueSky posts and provides previews of their content.

## Features

- Monitors channels for bsky.app links
- Displays post content and author information
- Configurable per-channel basis
- Minimal and unobtrusive output format

## Requirements

- Limnoria IRC Bot
- Python 3.6 or higher
- Required Python packages:
  - requests
  - beautifulsoup4

## Installation

1. Install the required Python packages:
   ```bash
   pip install requests beautifulsoup4
   ```

2. Clone this repository into your Limnoria plugin directory:
   ```bash
   cd /path/to/your/bot/plugins
   git clone git@github.com:Nelluk/BlueSky.git
   ```

3. Load the plugin in your Limnoria bot:
   ```
   /msg yourbot load BlueSky
   ```

## Configuration

To enable the plugin in a channel:

1. Enable the plugin for a specific channel:
   ```
   /msg yourbot config plugins.BlueSky.enabledChannels add #yourchannel
   ```

2. To disable the plugin for a channel:
   ```
   /msg yourbot config plugins.BlueSky.enabledChannels remove #yourchannel
   ```

3. To view current enabled channels:
   ```
   /msg yourbot config plugins.BlueSky.enabledChannels
   ```

## Usage

Once enabled in a channel, the plugin will automatically detect BlueSky links and display their content. No additional commands are needed.

Example output:
```
<user> https://bsky.app/profile/jburnmurdoch.bsky.social/post/...
<bot> A tale of two platforms: BlueSky user numbers have hit a new record high in recent days, while the number of people deleting their accounts on X/Twitter has rocketed 🚀 -- John Burn-Murdoch (@jburnmurdoch.bsky.social)
```
