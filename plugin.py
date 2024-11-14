import supybot.callbacks as callbacks
import supybot.ircmsgs as ircmsgs
from supybot.commands import *
import supybot.log as log
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

class BlueSky(callbacks.Plugin):
    """BlueSky link preview plugin for Supybot/Limnoria.
    
    This plugin monitors IRC channels for BlueSky post URLs and generates previews by:
    1. Extracting post content and author information from meta tags
    2. Removing unnecessary formatting like newlines and quote indicators
    3. Adding the post's publication date
    4. Formatting everything into a clean, single-line response
    
    The plugin uses BeautifulSoup for HTML parsing and handles various error cases
    gracefully with appropriate logging.
    """
    threaded = True

    def __init__(self, irc):
        super().__init__(irc)
        # Matches BlueSky post URLs in the format: https://bsky.app/profile/user/post/id
        self.bsky_pattern = re.compile(r'https?://(?:www\.)?bsky\.app/profile/[^/]+/post/[^/\s]+')
        # Matches embedded content indicators like "[contains quote post]"
        self.quote_pattern = re.compile(r'\[contains (?:quote|post|embedded content)[^\]]*\]')

    def doPrivmsg(self, irc, msg):
        """Handle incoming IRC messages by checking for BlueSky URLs."""
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
        """Fetch and parse BlueSky post metadata.
        
        Args:
            url: The BlueSky post URL to fetch
            
        Returns:
            str: Formatted post content with author info and timestamp, or None if parsing fails
            
        The returned string format is:
        "Post content -- Author (@handle.bsky.social) [YYYY-MM-DD]"
        """
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract post content and author info
        post_content = None
        author_info = None
        timestamp = None
        
        # Try to get content from meta tags
        for meta in soup.find_all('meta'):
            if meta.get('property') == 'og:description' or meta.get('name') == 'description':
                content = meta.get('content')
                if content:
                    # Remove newlines and quote indicators
                    content = content.replace('\n\n', ' ').replace('\n', ' ')
                    content = self.quote_pattern.sub('', content).strip()
                    post_content = content
            elif meta.get('name') == 'article:published_time':
                # Extract date portion (YYYY-MM-DD) from timestamp
                timestamp = meta.get('content', '').split('T')[0]
        
        # Get author info from og:title
        title_meta = soup.find('meta', property='og:title')
        if title_meta:
            author_info = title_meta.get('content')
        
        if not post_content or not author_info:
            return None
            
        # Format the output with timestamp if available
        if timestamp:
            return f"{post_content} -- {author_info} [{timestamp}]"
        else:
            return f"{post_content} -- {author_info}"

Class = BlueSky
