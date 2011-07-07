import unittest


import sys; sys.path.append("../src")
try:
    import event
except:
    print "Unable to import 'event' module."


class TestOneEventPerLine(unittest.TestCase):
    def testMostSimpleEvent(self):
        line = 'go there and get me some food.'
        conf = {'events_config' : [{'eventtype' : 'my-wonderful-type',
                                    'regexps' : ['.*foo.*']}]}
        event = create_event(line, conf)
        expected_event = {'eventtype' : 'my-wonderful-type', 'line' : line}
        self.assertDictEqual(expected_event, event)


    def testWithUserDefinedAndGlobalConfs(self):
        line = 'lex parsimoniae'
        conf = {
           'global_fields': {
               'host': 'my-machine',
               'log_type': 'apache',
           },
           'events_config': [{
                'eventtype': 'acessos',
                'regexps': ['^lex.*$'],
                'one_event_per_line_conf': {
                    'user_defined_fields': {
                    'passo': 'passo 1',
                    'produto': 'antivirus'}
                }
            }],
        }
        event = create_event(line, conf)
        expected_subset = {'host' : 'my-machine', 'log_type' : 'apache', 
                           'passo' : 'passo 1', 'produto' : 'antivirus'}
        self.assertDictContainsSubset(expected_subset, event)


    def testWithoutRegexps(self):
        line = 'imagination is more important than knowledge'
        conf = {'events_config' : [{'eventtype' : 'my-wonderful-type'}]}
        with self.assertRaises('RegexpsNotFound'):
            create_event(line, conf)


    def testWithEmptyListOfRegexps(self):
        line = 'go, go, go, marine!'
        conf = {'events_config' : [{'eventtype' : 'my-wonderful-type',
                                    'regexps' : []}]}
        event = create_event(line, conf)
        expected_event = None
        self.assertDictEqual(expected_event, event)


    def testEventWithRegexpGroups(self):
        line = 'There\'s nothing you can do that can\'t be done'
        conf = {'events_config' : [{'eventtype' : 'my-wonderful-type',
                                    'regexps' : ['.*(?P<who>you).*(?P<verb>can).*']}]}
        event = create_event(line, conf)
        self.assertDictContainsSubset({'who' : 'you', 'verb' : 'can'}, event)

        
#TODO: melhorar organizacao dos confs

if __name__ == "__main__":
    unittest.main()
