import supybot.callbacks as callbacks
import supybot.ircmsgs as ircmsgs
from supybot.commands import *
import supybot.log as log
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

class BlueSky(callbacks.Plugin):
    """BlueSky link preview plugin"""
    threaded = True

    def __init__(self, irc):
        super().__init__(irc)
        self.bsky_pattern = re.compile(r'https?://(?:www\.)?bsky\.app/profile/[^/]+/post/[^/\s]+')

    def doPrivmsg(self, irc, msg):
        channel = msg.args[0]
        enabled_channels = self.registryValue('enabledChannels')
        
        if channel not in enabled_channels:
            return
            
        message = msg.args[1]
        matches = self.bsky_pattern.finditer(message)
        
        for match in matches:
            url = match.group(0)
            try:
                preview = self._fetch_preview(url)
                if preview:
                    irc.reply(preview, prefixNick=False)
            except requests.RequestException as e:
                log.debug('BlueSky: Failed to fetch URL: %s', str(e))
                irc.reply('Error: Could not fetch BlueSky post', prefixNick=False)
            except Exception as e:
                log.debug('BlueSky: Unexpected error: %s', str(e))
                irc.reply('Error: Could not process BlueSky post', prefixNick=False)

    def _fetch_preview(self, url):
        """Fetch and parse BlueSky post metadata."""
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract post content and author info
        post_content = None
        author_info = None
        
        # Try to get content from meta tags
        for meta in soup.find_all('meta'):
            if meta.get('property') == 'og:description' or meta.get('name') == 'description':
                content = meta.get('content')
                if content:
                    post_content = content
                    break
        
        # Get author info from og:title
        title_meta = soup.find('meta', property='og:title')
        if title_meta:
            author_info = title_meta.get('content')
        
        if not post_content or not author_info:
            return None
            
        # Format the output
        return f"{post_content} -- {author_info}"

Class = BlueSky
