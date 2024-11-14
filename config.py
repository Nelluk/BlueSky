import supybot.conf as conf
import supybot.registry as registry

def configure(advanced):
    from supybot.questions import output, expect, anything, something, yn
    conf.registerPlugin('BlueSky', True)

BlueSky = conf.registerPlugin('BlueSky')

conf.registerGlobalValue(BlueSky, 'enabledChannels',
    registry.SpaceSeparatedListOfStrings([], """List of channels where the 
    BlueSky link preview feature is enabled."""))
