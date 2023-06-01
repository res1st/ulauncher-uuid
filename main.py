from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.client.Extension import Extension
from ulauncher.api.shared.action.CopyToClipboardAction import CopyToClipboardAction
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.event import KeywordQueryEvent, PreferencesUpdateEvent, PreferencesEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem

import logging
import uuid
import ArgumentMatcher

logger = logging.getLogger(__name__)


class UuidExt(Extension):

    def __init__(self):
        logger.info('initiaiize UuidExt')
        super(UuidExt, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())
        self.subscribe(PreferencesUpdateEvent, PreferencesUpdateEventListener())
        self.subscribe(PreferencesEvent, PreferencesEventListener())


class KeywordQueryEventListener(EventListener):

    def on_event(self, event, extension):
        logger.info('event UuidExt: %s', event)
        resultItems = []
        uuids = []
        
        setting_upper = extension.uuid_uppercase
        setting_hyphons = extension.uuid_remove_hyphons
 
        arguments_unparsed = event.get_argument()
        arguments = ArgumentMatcher.Arguments(arguments_unparsed)

        uuidsV1 =  ""
        uuidsV4 =  ""
        for _ in range(arguments.count):
            uuidsV1 += process_uuid(str(uuid.uuid1()), setting_upper, setting_hyphons)
            uuidsV4 += process_uuid(str(uuid.uuid4()), setting_upper, setting_hyphons)
            if arguments.seperator is not None:
                uuidsV1 += arguments.seperator
                uuidsV4 += arguments.seperator
        
        # remove trailing seperator
        if arguments.seperator is not None:
            uuidsV1 = uuidsV1[:-1]
            uuidsV4 = uuidsV4[:-1]

        # first insert v4 because it is the better default        
        uuids.append(["v4 (random)", uuidsV4])
        uuids.append(["v1 (MAC/date based)", uuidsV1])

        if arguments_unparsed is not None and arguments.seperator is None:
            uuids.append(["v3 DNS", process_uuid(str(uuid.uuid3(uuid.NAMESPACE_DNS, arguments_unparsed)), setting_upper, setting_hyphons)])
            uuids.append(["v3 URL", process_uuid(str(uuid.uuid3(uuid.NAMESPACE_URL, arguments_unparsed)), setting_upper, setting_hyphons)])
            uuids.append(["v5 DNS", process_uuid(str(uuid.uuid5(uuid.NAMESPACE_DNS, arguments_unparsed)), setting_upper, setting_hyphons)])
            uuids.append(["v5 URL", process_uuid(str(uuid.uuid5(uuid.NAMESPACE_URL, arguments_unparsed)), setting_upper, setting_hyphons)])

        for description, genUuid in uuids:
            # genUuid = process_uuid(genUuid, extension.uuid_uppercase, extension.uuid_remove_hyphons)
            
            resultItems.append(ExtensionResultItem(icon='images/uuid.png',
                                             name=genUuid,
                                             description=description,
                                             highlightable=False,
                                             on_enter=CopyToClipboardAction(genUuid)
                                             ))
        return RenderResultListAction(resultItems)


def process_uuid(gen_uuid, upper, remove_hyphons):
    if upper == "True":
        gen_uuid = gen_uuid.upper()

    if remove_hyphons == "True":
        gen_uuid = gen_uuid.replace("-", "")
    return gen_uuid

class PreferencesUpdateEventListener(EventListener):

    def on_event(self, event, extension):

        if event.id == "uuid_uppercase":
            extension.uuid_uppercase = event.new_value
        elif event.id == "uuid_remove_hyphons":
            extension.uuid_remove_hyphons = event.new_value

class PreferencesEventListener(EventListener):

    def on_event(self, event, extension):
        extension.uuid_uppercase = event.preferences["uuid_uppercase"]
        extension.uuid_remove_hyphons = event.preferences["uuid_remove_hyphons"]

if __name__ == '__main__':
    UuidExt().run()

