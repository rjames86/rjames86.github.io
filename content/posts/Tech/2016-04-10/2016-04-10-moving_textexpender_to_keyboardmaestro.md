Title: Moving TextExpander Snippets to Keyboard Maestro
Date: 2016-04-10 17:26
Category: Tech
Tags: scripting, textexpander, python, keyboardmaestro
Author: Ryan M

I've been a long time TextExpander user. I use it every day for simple things like pasting my contact info or shortening urls using bit.ly. There are plenty of articles out there arguing for and against TextExpander's new subscription model. I support their decision but I can't justify $50 a year's worth of value and so I'm moving all of my snippets to Keyboard Maestro.
<!-- PELICAN_END_SUMMARY -->  

I had been thinking this weekend whether it would be worth the time to try to migrate all my snippets to Keyboard Maestro. Browsing my Twitter feed, it looked as though [Dr. Drang][drang] had beat me to it. Unfortunately he didn't do the work I was hoping I wouldn't have to do, and so I sat down to see how hard it would be to convert snippets to macros. Turns out...not that hard.

Here are the requirements for running this script:

- Python 2.7 (I didn't test Python 3.x). If you're running an older/newer version of Python, you should be able to replace `python` with `/usr/bin/python2.7` when running the script.
- TextExpander 5.x. If you are running version 4, your settings will be named Settings.textexpander instead of Settings.textexpandersettings.

I've made some decisions as to how I want the snippets to work. Notably

- Pasting instead of typing. Typing is too slow.
- Delete the last clipboard item, since it was the text that was just pasted. 
- Groups remain the same. If you used groups in TextExpander, they show up as "Snippets - <group name>" in Keyboard Maestro. 

There are a few things that I haven't yet solved. Some I might in the future, others maybe not:

- I didn't test Applescript since I didn't have any. Please let me know if that one breaks.
- Placeholders and variables from TextExpander won't work. This means if you had a "today's date" snippet, you'll need to rewrite that one[^1].
- Custom delimiters. I haven't really figured out if there's a way to do this. I've tried changing Keyboard Maestro to only fire on delimiters, but it doesn't seem to work. If anyone figured this out, please let me know.


Before running, be sure to update the variable `TEXTEXPANDER_PATH` to wherever your TextExpander settings file lives. To run, it's as simple as navigating to the location where the script lives in Terminal.app and entering

	python TE.py

You'll now have a folder on your Desktop named 'TextExpander_to_KeyboardMaestro' with all of your groups.

----

*Update 2016-04-12*

Big thanks to NW in the comments for helping me debug a few things.

I've removed the import of `enum`. I had forgotten that wasn't a standard library in Python 2.7. I also added a list of requirements above for running the script.

*Update 2016-04-14*

Also thanks to Dr Drang for posting about the script! I've made some updates and also put up a repo for those who would like to make edits and pull requests.

Updates are

- Optional prefix if you want to change that up when moving to Keyboard Maestro
- Insert text by typing OR pasting
- Added some instruction on how to edit the variables to have the script do what you want

The repo is now hosted at [https://github.com/rjames86/textexpander_to_keyboardmaestro](https://github.com/rjames86/textexpander_to_keyboardmaestro)

----


You can download the script on Github [here](https://raw.githubusercontent.com/rjames86/textexpander_to_keyboardmaestro/master/TE.py)

    import plistlib
    import os
    import glob

    '''
    This script will parse through all group_*.xml files within your TextExpander folder.
    Anything marked as Plain Text, Shell Script or JavaScript should be converted into
    Keyboard Maestro groups with the same title and abbreviation.

    All new KM Macro files will be saved to the Desktop.

    '''

    # Modify this area to customize how the script will run

    # Change this path to where ever your TextExander Settings live
    HOME = os.path.expanduser('~')
    TEXTEXPANDER_PATH = HOME + '/Dropbox/TextExpander/Settings.textexpandersettings'
    SAVE_PATH = HOME + '/Desktop/TextExpander_to_KeyboardMaestro'

    # Change this if you'd like to change your snippets when importing to Keyboard Maestro
    # If your snippet is ttest, you can make it ;;ttest by changing the variable to ';;'
    OPTIONAL_NEW_PREFIX = ''

    # Change this if you want the snippet to inserted by typing or pasting
    # Remember it MUST be 'paste' or 'type' or the script will fail
    PASTE_OR_TYPE = 'paste' # 'type'




    ############

    # Edit below at your own risk

    ############

    snippet_types = {
        'plaintext': 0,
        'applescript': 2,
        'shell': 3,
        'javascript': 4,
    }

    snippet_types_to_values = dict((value, key) for key, value in snippet_types.iteritems())


    class KeyboardMaestroMacros(object):
        @classmethod
        def macro_by_name(cls, macro_name, group_name, name, text, abbreviation):
            return getattr(cls, macro_name)(group_name, name, text, abbreviation)

        @staticmethod
        def javascript(group_name, name, text, abbreviation):
            return {
                'Activate': 'Normal',
                'CreationDate': 0.0,
                'IsActive': True,
                'Macros': [
                    {'Actions': [
                        {'DisplayKind': KeyboardMaestroMacros._paste_or_type(),
                         'IncludeStdErr': True,
                         'IsActive': True,
                         'IsDisclosed': True,
                         'MacroActionType': 'ExecuteJavaScriptForAutomation',
                         'Path': '',
                         'Text': text,
                         'TimeOutAbortsMacro': True,
                         'TrimResults': True,
                         'TrimResultsNew': True,
                         'UseText': True}, {
                            'IsActive': True,
                            'IsDisclosed': True,
                            'MacroActionType': 'DeletePastClipboard',
                            'PastExpression': '0'}
                        ],
                     'CreationDate': 482018934.65354,
                     'IsActive': True,
                     'ModificationDate': 482018953.856014,
                     'Name': name,
                     'Triggers': [{
                        'Case': 'Exact',
                        'DiacriticalsMatter': True,
                        'MacroTriggerType': 'TypedString',
                        'OnlyAfterWordBreak': False,
                        'SimulateDeletes': True,
                        'TypedString': KeyboardMaestroMacros._abbreviation(abbreviation)}]}
                ],
                'Name': 'Snippet - %s' % group_name,
            }

        @staticmethod
        def applescript(group_name, name, text, abbreviation):
            return {
                'Activate': 'Normal',
                'CreationDate': 0.0,
                'IsActive': True,
                'Macros': [
                    {'Actions': [
                        {'DisplayKind': KeyboardMaestroMacros._paste_or_type(),
                         'IncludeStdErr': True,
                         'IsActive': True,
                         'IsDisclosed': True,
                         'MacroActionType': 'ExecuteAppleScript',
                         'Path': '',
                         'Text': text,
                         'TimeOutAbortsMacro': True,
                         'TrimResults': True,
                         'TrimResultsNew': True,
                         'UseText': True}, {
                            'IsActive': True,
                            'IsDisclosed': True,
                            'MacroActionType': 'DeletePastClipboard',
                            'PastExpression': '0'}
                        ],
                     'CreationDate': 482018934.65354,
                     'IsActive': True,
                     'ModificationDate': 482018953.856014,
                     'Name': name,
                     'Triggers': [{
                        'Case': 'Exact',
                        'DiacriticalsMatter': True,
                        'MacroTriggerType': 'TypedString',
                        'OnlyAfterWordBreak': False,
                        'SimulateDeletes': True,
                        'TypedString': KeyboardMaestroMacros._abbreviation(abbreviation)}]}
                ],
                'Name': 'Snippet - %s' % group_name,
            }

        @staticmethod
        def plaintext(group_name, name, text, abbreviation):
            return {
                'Activate': 'Normal',
                'CreationDate': 0.0,
                'IsActive': True,
                'Macros': [{'Actions': [
                    {
                        'Action': KeyboardMaestroMacros._paste_or_type('plaintext'),
                        'IsActive': True,
                        'IsDisclosed': True,
                        'MacroActionType': 'InsertText',
                        'Paste': True,
                        'Text': text}, {
                            'IsActive': True,
                            'IsDisclosed': True,
                            'MacroActionType': 'DeletePastClipboard',
                            'PastExpression': '0'
                        }],
                    'CreationDate': 0.0,
                    'IsActive': True,
                    'ModificationDate': 482031702.132113,
                    'Name': name,
                    'Triggers': [{
                        'Case': 'Exact',
                        'DiacriticalsMatter': True,
                        'MacroTriggerType': 'TypedString',
                        'OnlyAfterWordBreak': False,
                        'SimulateDeletes': True,
                        'TypedString': KeyboardMaestroMacros._abbreviation(abbreviation)}],
                }],
                'Name': 'Snippet - %s' % group_name,
            }

        @staticmethod
        def shell(group_name, name, text, abbreviation):
            return {
                'Activate': 'Normal',
                'CreationDate': 0.0,
                'IsActive': True,
                'Macros': [{
                    'Actions': [{
                        'DisplayKind': KeyboardMaestroMacros._paste_or_type(),
                        'IncludeStdErr': True,
                        'IsActive': True,
                        'IsDisclosed': True,
                        'MacroActionType': 'ExecuteShellScript',
                        'Path': '',
                        'Text': text,
                        'TimeOutAbortsMacro': True,
                        'TrimResults': True,
                        'TrimResultsNew': True,
                        'UseText': True},
                     {'IsActive': True,
                      'IsDisclosed': True,
                      'MacroActionType': 'DeletePastClipboard',
                      'PastExpression': '0'}],
                    'CreationDate': 482018896.698121,
                    'IsActive': True,
                    'ModificationDate': 482020783.300151,
                    'Name': name,
                    'Triggers': [{
                        'Case': 'Exact',
                        'DiacriticalsMatter': True,
                        'MacroTriggerType': 'TypedString',
                        'OnlyAfterWordBreak': False,
                        'SimulateDeletes': True,
                        'TypedString': KeyboardMaestroMacros._abbreviation(abbreviation)}],
                    }],
                'Name': 'Snippet - %s' % group_name,
            }

        @staticmethod
        def _abbreviation(name):
            return OPTIONAL_NEW_PREFIX + name

        @staticmethod
        def _paste_or_type(snippet_type=None):
            value = {
                'paste': "Pasting",
                'type': "Typing"
            }
            if snippet_type == 'plaintext':
                return "By%s" % value[PASTE_OR_TYPE]
            else:
                return value[PASTE_OR_TYPE]


    def parse_textexpander():
        '''
        Each TextExpander group is its own file starting with the file name 'group_'.

        Example snippet dictionary
        {
            'abbreviation': '.bimg',
            'abbreviationMode': 0,
            'creationDate': datetime.datetime(2013, 5, 19, 19, 42, 16),
            'label': '',
            'modificationDate': datetime.datetime(2015, 1, 10, 20, 19, 59),
            'plainText': 'some text,
            'snippetType': 3,
            'uuidString': '100F8D1F-A2D1-4313-8B55-EFD504AE7894'
        }

        Return a list of dictionaries where the keys are the name of the group
        '''
        to_ret = {}

        # Let's get all the xml group files in the directory
        xml_files = [f for f in glob.glob(TEXTEXPANDER_PATH + "/*.xml")
                     if f.startswith(TEXTEXPANDER_PATH + "/group_")]

        for xml_file in xml_files:
            pl = plistlib.readPlist(xml_file)
            if pl['name'] not in to_ret:
                to_ret[pl['name']] = []
            for snippet in pl['snippetPlists']:
                if snippet['snippetType'] in snippet_types.values():
                    to_ret[pl['name']].append(snippet)
        return to_ret


    def main():
        text_expanders = parse_textexpander()
        for group, text_expander in text_expanders.iteritems():
            macros_to_create = []
            for snippet in text_expander:
                macros_to_create.append(
                    KeyboardMaestroMacros.macro_by_name(snippet_types_to_values[snippet['snippetType']],
                                                        group,
                                                        snippet['label'],
                                                        snippet['plainText'],
                                                        snippet['abbreviation'])
                    )

            # Create a new folder on the desktop to put the macros
            if not os.path.exists(SAVE_PATH):
                os.mkdir(SAVE_PATH)
            # Save the macros
            with open(SAVE_PATH + '/%s.kmmacros' % group, 'w') as f:
                f.write(plistlib.writePlistToString(macros_to_create))

    if __name__ == '__main__':
        main()




Feedback and pull requests welcome. I'll continue to update the script and this post if I make any substantial iterations.

[drang]: http://leancrew.com/all-this/2016/04/importing-textexpander-snippets-to-keyboard-maestro/


[^1]: Hint. If you had your date look like 2016-04-10, the Keyboard Maestro equivalent is `%ICUDateTime%yyyy-MM-dd%`
