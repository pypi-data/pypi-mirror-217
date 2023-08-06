import json
from swibots.api.auth.models.auth_user import AuthUser
from swibots.api.community.events import *
from swibots.base import SwitchRestClient, SwitchWSAsyncClient
from swibots.config import get_config
from swibots.error import SwitchError
from swibots.utils.ws.asyncstomp.async_ws_subscription import AsyncWsSubscription
from swibots.utils.ws.common.ws_message import WsMessage
from swibots.types import EventType
from .controllers import ChannelController, GroupController, CommunityController
import swibots


class CommunityClient(SwitchRestClient):
    def __init__(
        self,
        app: "swibots.App" = None,
        base_url: str = None,
        ws_url: str = None,
    ):
        base_url = base_url or get_config()["COMMUNITY_SERVICE"]["BASE_URL"]
        self._ws_url = ws_url or get_config()["COMMUNITY_SERVICE"]["WS_URL"]
        super().__init__(app, base_url)
        self._channels = None
        self._groups = None
        self._communities = None
        self._ws: SwitchWSAsyncClient = None
        self._started = False

    @property
    def channels(self) -> ChannelController:
        """Get the channels controller"""
        if self._channels is None:
            self._channels = ChannelController(self)
        return self._channels

    @property
    def groups(self) -> GroupController:
        """Get the channels controller"""
        if self._groups is None:
            self._groups = GroupController(self)
        return self._groups

    @property
    def communities(self) -> CommunityController:
        """Get the channels controller"""
        if self._communities is None:
            self._communities = CommunityController(self)
        return self._communities

    @property
    def ws(self) -> SwitchWSAsyncClient:
        if self._ws is None:
            self._ws = SwitchWSAsyncClient(self._ws_url, self.token)
        return self._ws

    @property
    async def subscribe(self, endpoint: str, callback=None) -> AsyncWsSubscription:
        if self.user is None:
            raise SwitchError("User is not set")
        if callback is None:
            raise SwitchError("Callback is not set")
        return await self.ws.subscribe(endpoint, callback=callback)

    async def subscribe_to_notifications(self, callback=None) -> AsyncWsSubscription:
        subscription = await self.ws.subscribe(
            "/user/queue/events",
            callback=lambda event: callback(self._parse_event(event)),
        )
        return subscription

    def _parse_event(self, raw_message: WsMessage) -> CommunityEvent:
        json_data = json.loads(raw_message.body)
        type = json_data.get("type", "COMMUNITY")
        evt = None
        if type == EventType.COMMUNITY_CHANNEL_CREATE.value:
            evt = self.build_object(ChannelCreatedEvent, json_data)
            # return ChannelCreatedEvent.build_from_json(json_data)
        elif type == EventType.COMMUNITY_CHANNEL_UPDATE.value:
            evt = self.build_object(ChannelUpdatedEvent, json_data)
            # return ChannelUpdatedEvent.build_from_json(json_data)
        elif type == EventType.COMMUNITY_CHANNEL_DELETE.value:
            evt = self.build_object(ChannelDeletedEvent, json_data)
            # return ChannelDeletedEvent.build_from_json(json_data)
        elif type == EventType.COMMUNITY_UPDATE.value:
            evt = self.build_object(CommunityUpdatedEvent, json_data)
            # return CommunityUpdatedEvent.build_from_json(json_data)
        elif type == EventType.COMMUNITY_GROUP_CREATE.value:
            evt = self.build_object(GroupCreatedEvent, json_data)
            # return GroupCreatedEvent.build_from_json(json_data)
        elif type == EventType.COMMUNITY_GROUP_UPDATE.value:
            evt = self.build_object(GroupUpdatedEvent, json_data)
            # return GroupUpdatedEvent.build_from_json(json_data)
        elif type == EventType.COMMUNITY_GROUP_DELETE.value:
            evt = self.build_object(GroupDeletedEvent, json_data)
            # return GroupDeletedEvent.build_from_json(json_data)
        elif type == EventType.COMMUNITY_USER_BAN.value:
            evt = self.build_object(UserBannedEvent, json_data)
            # return UserBannedEvent.build_from_json(json_data)
        elif type == EventType.COMMUNITY_MEMBER_JOIN.value:
            evt = self.build_object(MemberJoinedEvent, json_data)
            # return MemberJoinedEvent.build_from_json(json_data)
        elif type == EventType.COMMUNITY_MEMBER_LEAVE.value:
            evt = self.build_object(MemberLeftEvent, json_data)
            # return MemberLeftEvent.build_from_json(json_data)
        else:
            evt = self.build_object(CommunityEvent, json_data)

        return evt

    async def start(self):
        """Start the community client"""
        if self.user is None:
            raise SwitchError("User is not set")
        await self.ws.connect()
        self._started = True

    async def stop(self):
        if self._started:
            await self.ws.disconnect()
            self._started = False
